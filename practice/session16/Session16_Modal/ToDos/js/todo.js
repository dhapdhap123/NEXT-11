const todoForm = document.getElementById("todo-form");
const todoList = document.getElementById("todo-list");
const submitBtn = document.querySelector(".submitBtn");

const onDeleteTodo = (e) => {
  e.preventDefault();
  console.log("삭제");
};

const renderTodos = () => {
  const todos = window.localStorage.getItem("todos");
  const todos_parsed = JSON.parse(todos);
  for (i in todos_parsed) {
    const li = document.createElement("li");
    li.innerHTML = `<span>${todos_parsed[i]}</span><button onClick="onDeleteTodo">X</button>`;
    todoList.appendChild(li);
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
  li.innerText = new_todo;
  todoList.appendChild(li);

  content.value = "";
};

renderTodos();

todoForm.addEventListener("submit", onCreateTodo);
