const BASE = "/api/todos";

export async function getTodos() {
  const res = await fetch(BASE);
  return res.json();
}

export function createTodo(title) {
  return fetch(BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
}

export const toggleTodo = (id) => fetch(`${BASE}/${id}`, { method: "PATCH" });
export const removeTodo = (id) => fetch(`${BASE}/${id}`, { method: "DELETE" });
