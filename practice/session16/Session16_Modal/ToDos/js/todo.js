const todoForm = document.getElementById("todo-form");
const todoList = document.getElementById("todo-list");
const submitBtn = document.querySelector(".submitBtn");

let li_num = 0;

const onDeleteTodo = (e) => {
  const todos = window.localStorage.getItem("todos");
  const todos_parsed = JSON.parse(todos);
  const li_id = e.target.id;
  for (i in todos_parsed) {
    if (i === li_id) {
      todos_parsed.splice(i, 1);
    }
  }
  const li_delete = document.getElementById(`${li_id}li`);
  li_delete.remove();
  window.localStorage.setItem("todos", JSON.stringify(todos_parsed));
};

const renderTodos = () => {
  const todos = window.localStorage.getItem("todos");
  const todos_parsed = JSON.parse(todos);
  for (i in todos_parsed) {
    const li = document.createElement("li");
    li.id = li_num + "li";
    li.innerHTML = `<span id=${li_num}>${todos_parsed[i]}</span><button id=${li_num} onclick="onDeleteTodo(event)">X</button>`;
    todoList.appendChild(li);
    li_num += 1;
  }
};

const onCreateTodo = (e) => {
  e.preventDefault();
  const content = document.getElementById("content");

  const todos = window.localStorage.getItem("todos");
  const todos_parsed = JSON.parse(todos);
  const new_todo = content.value;
  const new_todos = [...todos_parsed, new_todo];

  window.localStorage.setItem("todos", JSON.stringify(new_todos));

  const li = document.createElement("li");
  li.id = li_num + "li";
  li.innerHTML = `<span id=${li_num}>${new_todo}</span><button id=${li_num} onclick="onDeleteTodo(event)">X</button>`;
  li_num += 1;
  todoList.appendChild(li);

  content.value = "";
};

renderTodos();

todoForm.addEventListener("submit", onCreateTodo);
