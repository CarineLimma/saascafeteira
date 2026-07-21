

document.addEventListener("DOMContentLoaded", () => {

    console.log("Auth carregado");

    configurarMostrarSenha();
    validarFormulario();
    verificarForcaSenha();

});

function validarFormulario() {

    const form = document.querySelector("form");

    if (!form) return;

    form.addEventListener("submit", (e) => {

        const inputs = form.querySelectorAll("input[required]");

        let valido = true;

        inputs.forEach(input => {

            if (input.value.trim() === "") {

                valido = false;

                input.style.borderColor = "#dc3545";

            } else {

                input.style.borderColor = "";

            }

        });

        if (!valido) {

            e.preventDefault();

            alert("Preencha todos os campos.");

        }

    });

}

function verificarForcaSenha() {

    const senha = document.getElementById("senha");

    if (!senha) return;

    const indicador = document.createElement("small");

    indicador.style.display = "block";
    indicador.style.marginTop = "8px";

    senha.parentElement.appendChild(indicador);

    senha.addEventListener("input", () => {

        const valor = senha.value;

        if (valor.length < 6) {

            indicador.innerHTML = "🔴 Senha fraca";
            indicador.style.color = "#ff6b6b";

        } else if (valor.length < 10) {

            indicador.innerHTML = "🟡 Senha média";
            indicador.style.color = "#ffd166";

        } else {

            indicador.innerHTML = "🟢 Senha forte";
            indicador.style.color = "#8ce99a";

        }

    });

}