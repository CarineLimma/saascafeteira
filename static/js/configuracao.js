// =========================================
// CONFIGURAÇÃO DO SISTEMA
// =========================================

// Aguarda o carregamento da página
document.addEventListener("DOMContentLoaded", () => {
  inicializarConfiguracoes();
});

// =========================================
// INICIALIZAÇÃO
// =========================================
function inicializarConfiguracoes() {
  carregarTema();
  configurarEventos();
}

// =========================================
// EVENTOS
// =========================================
function configurarEventos() {
  // Toggle de tema (se existir no HTML)
  const toggleTema = document.getElementById("toggle-tema");

  if (toggleTema) {
    toggleTema.addEventListener("change", () => {
      if (toggleTema.checked) {
        ativarTemaEscuro();
      } else {
        ativarTemaClaro();
      }
    });
  }

  // Botão salvar configurações
  const btnSalvar = document.getElementById("btn-salvar-config");

  if (btnSalvar) {
    btnSalvar.addEventListener("click", salvarConfiguracoes);
  }
}

// =========================================
// TEMA
// =========================================
function ativarTemaEscuro() {
  document.body.classList.add("dark-mode");
  localStorage.setItem("tema", "dark");
}

function ativarTemaClaro() {
  document.body.classList.remove("dark-mode");
  localStorage.setItem("tema", "light");
}

function carregarTema() {
  const temaSalvo = localStorage.getItem("tema");

  if (temaSalvo === "dark") {
    document.body.classList.add("dark-mode");

    const toggleTema = document.getElementById("toggle-tema");
    if (toggleTema) {
      toggleTema.checked = true;
    }
  }
}

// =========================================
// SALVAR CONFIGURAÇÕES
// =========================================
function salvarConfiguracoes() {
  const nomeSistema = document.getElementById("nome-sistema")?.value;
  const emailContato = document.getElementById("email-contato")?.value;

  if (nomeSistema) {
    localStorage.setItem("nomeSistema", nomeSistema);
  }

  if (emailContato) {
    localStorage.setItem("emailContato", emailContato);
  }

  mostrarMensagem("Configurações salvas com sucesso!");
}

// =========================================
// FEEDBACK VISUAL
// =========================================
function mostrarMensagem(texto) {
  let msg = document.createElement("div");
  msg.className = "toast-sucesso";
  msg.innerText = texto;

  document.body.appendChild(msg);

  setTimeout(() => {
    msg.classList.add("show");
  }, 100);

  setTimeout(() => {
    msg.classList.remove("show");

    setTimeout(() => {
      msg.remove();
    }, 300);
  }, 2500);
}