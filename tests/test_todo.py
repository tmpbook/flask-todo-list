import unittest
from app import app
from app.models import Todo
from werkzeug.exceptions import HTTPException


class TodoTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        # clear data for each test
        todos = Todo.objects.all()
        for todo in todos:
            todo.delete()

    def test_index(self):
        rv = self.app.get('/')
        assert "awesome-flask-todo" in rv.data

    def test_empty(self):
        rv = self.app.get('/')
        assert "No todos, please add" in rv.data

    def test_add_todo(self):
        self.app.post("/add", data=dict(content="test add todo"))
        todo = Todo.objects.get_or_404(content="test add todo")
        assert todo is not None

    def test_none_todo(self):
        try:
            todo = Todo.objects.get_or_404(content='test todo none')
        except HTTPException as e:
            assert e.code == 404

    def test_done_todo(self):
        todo = Todo(content='test done todo')
        todo.save()
        url = '/done/'+str(todo.id)
        rv = self.app.get(url)
        assert '/undone/'+str(todo.id) in rv.data

    def test_undone_todo(self):
        todo = Todo(content='test undone todo')
        todo.save()
        url = '/undone/'+str(todo.id)
        rv = self.app.get(url)
        assert '/done/'+str(todo.id) in rv.data

    def test_delete_todo(self):
        todo = Todo(content='test delete done')
        todo.save()
        url = '/delete/'+str(todo.id)
        rv = self.app.get(url)
        assert "No todos, please add" in rv.data

    def test_404(self):
        rv = self.app.get('/404test')
        assert "Not Found" in rv.data


