// =========================================
// USUÁRIO - LOGIN / CADASTRO
// =========================================

document.addEventListener("DOMContentLoaded", () => {
  configurarFormulario();
  configurarToggleSenha();
});

// =========================================
// VALIDAÇÃO DE FORMULÁRIO
// =========================================
function configurarFormulario() {
  const form = document.querySelector("form");

  if (!form) return;

  form.addEventListener("submit", function (e) {
    const inputs = form.querySelectorAll("input");
    let valido = true;

    inputs.forEach((input) => {
      if (input.type !== "submit" && input.value.trim() === "") {
        valido = false;
        input.classList.add("input-erro");
      } else {
        input.classList.remove("input-erro");
      }
    });

    if (!valido) {
      e.preventDefault();
      mostrarMensagem("Preencha todos os campos!", "erro");
    }
  });
}

// =========================================
// MOSTRAR / OCULTAR SENHA
// =========================================
function configurarToggleSenha() {
  const senhaInputs = document.querySelectorAll('input[type="password"]');

  senhaInputs.forEach((input) => {
    const wrapper = document.createElement("div");
    wrapper.classList.add("senha-wrapper");

    const toggle = document.createElement("span");
    toggle.innerHTML = "👁️";
    toggle.classList.add("toggle-senha");

    input.parentNode.insertBefore(wrapper, input);
    wrapper.appendChild(input);
    wrapper.appendChild(toggle);

    toggle.addEventListener("click", () => {
      if (input.type === "password") {
        input.type = "text";
        toggle.innerHTML = "🙈";
      } else {
        input.type = "password";
        toggle.innerHTML = "👁️";
      }
    });
  });
}

// =========================================
// MENSAGENS (ERRO / SUCESSO)
// =========================================
function mostrarMensagem(texto, tipo = "sucesso") {
  let msg = document.createElement("div");

  msg.classList.add("msg");

  if (tipo === "erro") {
    msg.classList.add("msg-erro");
  } else {
    msg.classList.add("msg-sucesso");
  }

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

// =========================================
// DESTACAR ERRO EM INPUT
// =========================================
document.addEventListener("input", (e) => {
  if (e.target.tagName === "INPUT") {
    e.target.classList.remove("input-erro");
  }
});