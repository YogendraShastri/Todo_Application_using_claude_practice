import { createTodo, getTodos, removeTodo, toggleTodo } from "./api.js";
import { renderTodos } from "./ui.js";

const form = document.getElementById("todo-form");
const input = document.getElementById("todo-input");
const list = document.getElementById("todo-list");

async function refresh() {
  renderTodos(list, await getTodos(), {
    onToggle: (id) => toggleTodo(id).then(refresh),
    onDelete: (id) => removeTodo(id).then(refresh),
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = input.value.trim();
  if (!title) return;
  input.value = "";
  await createTodo(title);
  refresh();
});

refresh();
