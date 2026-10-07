// Búsqueda en vivo: pide al servidor las tarjetas (HTML parcial) y las inyecta.
(() => {
  const form = document.getElementById("form-busqueda");
  const inputQ = document.getElementById("q");
  const inputCat = document.getElementById("categoria");
  const chips = document.querySelectorAll(".chip");
  const orden = document.getElementById("orden");
  const minEst = document.getElementById("min_estrellas");
  const contenedor = document.getElementById("resultados");
  let temporizador, controlador;

  async function buscar() {
    const params = new URLSearchParams({
      q: inputQ.value.trim(), categoria: inputCat.value,
      orden: orden.value, min_estrellas: minEst.value,
    });
    if (controlador) controlador.abort();
    controlador = new AbortController();
    contenedor.classList.add("cargando");
    try {
      const resp = await fetch(`/buscar?${params}`, { signal: controlador.signal });
      if (!resp.ok) throw new Error(resp.status);
      contenedor.innerHTML = await resp.text();
    } catch (e) {
      if (e.name !== "AbortError")
        contenedor.innerHTML = '<div class="col-12 text-center text-danger py-4">No se pudo cargar la búsqueda. Intenta de nuevo.</div>';
    } finally {
      contenedor.classList.remove("cargando");
    }
  }

  form.addEventListener("submit", (e) => { e.preventDefault(); buscar(); });
  inputQ.addEventListener("input", () => { clearTimeout(temporizador); temporizador = setTimeout(buscar, 300); });
  orden.addEventListener("change", buscar);
  minEst.addEventListener("change", buscar);

  chips.forEach((chip) => chip.addEventListener("click", () => {
    const activo = chip.classList.contains("activo");
    chips.forEach((c) => c.classList.remove("activo"));
    inputCat.value = activo ? "" : chip.dataset.categoria;   // clic otra vez = quitar filtro
    if (!activo) chip.classList.add("activo");
    buscar();
  }));

  // Si llega con filtros en la URL, sincroniza los selectores
  const p = new URLSearchParams(location.search);
  if (p.get("orden")) orden.value = p.get("orden");
  if (p.get("min_estrellas")) minEst.value = p.get("min_estrellas");
})();
