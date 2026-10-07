// Chat con actualización periódica (polling cada 2 s).
(() => {
  const caja = document.getElementById("chat");
  const id = caja.dataset.oferente;
  const lista = document.getElementById("msgs");
  const form = document.getElementById("chat-form");
  const input = document.getElementById("texto");
  let ultimo = 0;

  function pintar(m) {
    const div = document.createElement("div");
    div.className = "burbuja " + (m.emisor === "cliente" ? "mio" : "otro");
    div.textContent = m.texto;          // textContent evita inyección de HTML
    lista.appendChild(div);
  }

  async function cargar() {
    try {
      const r = await fetch(`/chat/${id}/mensajes?desde=${ultimo}`);
      if (r.status === 401 || r.redirected) return location.reload();
      const datos = await r.json();
      if (datos.length) {
        lista.querySelector(".chat-vacio")?.remove();
        datos.forEach((m) => { pintar(m); ultimo = Math.max(ultimo, m.id); });
        lista.scrollTop = lista.scrollHeight;
      } else if (!lista.children.length) {
        lista.innerHTML = '<div class="chat-vacio">Aún no hay mensajes.<br>Escribe para acordar precio, fecha y detalles.</div>';
      }
    } catch (_) { /* reintenta en el siguiente ciclo */ }
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const texto = input.value.trim();
    if (!texto) return;
    input.value = "";
    await fetch(`/chat/${id}/enviar`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ texto }),
    });
    cargar();
  });

  cargar();
  setInterval(cargar, 2000);
})();
