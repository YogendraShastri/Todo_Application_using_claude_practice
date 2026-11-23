const form = document.getElementById("todo-form");
const input = document.getElementById("todo-input");
const list = document.getElementById("todo-list");

async function fetchTodos() {
  const res = await fetch("/api/todos");
  const todos = await res.json();
  renderTodos(todos);
}

function renderTodos(todos) {
  list.innerHTML = "";
  todos.forEach((todo) => {
    const li = document.createElement("li");
    if (todo.done) li.className = "done";

    const dot = document.createElement("button");
    dot.className = "dot";
    dot.setAttribute("aria-label", todo.done ? "Mark as not done" : "Mark as done");
    dot.addEventListener("click", () => toggleTodo(todo.id));

    const label = document.createElement("span");
    label.className = "todo-title";
    label.textContent = todo.title;

    const delBtn = document.createElement("button");
    delBtn.className = "del-btn";
    delBtn.setAttribute("aria-label", "Delete task");
    delBtn.innerHTML =
      '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 3h6l1 2h4v2H4V5h4l1-2zm-3 6h12l-1 12H7L6 9z"/></svg>';
    delBtn.addEventListener("click", () => deleteTodo(todo.id));

    li.appendChild(dot);
    li.appendChild(label);
    li.appendChild(delBtn);
    list.appendChild(li);
  });
}

async function addTodo(title) {
  await fetch("/api/todos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  fetchTodos();
}

async function toggleTodo(id) {
  await fetch(`/api/todos/${id}`, { method: "PATCH" });
  fetchTodos();
}

async function deleteTodo(id) {
  await fetch(`/api/todos/${id}`, { method: "DELETE" });
  fetchTodos();
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const title = input.value.trim();
  if (!title) return;
  addTodo(title);
  input.value = "";
});

fetchTodos();
