const toggleSenha = document.getElementById("toggleSenha");
const senhaInput = document.getElementById("senha");

if(toggleSenha && senhaInput){

    toggleSenha.addEventListener("click", () => {

        const icon = toggleSenha.querySelector("i");

        if(senhaInput.type === "password"){

            senhaInput.type = "text";
            icon.classList.remove("bi-eye-fill");
            icon.classList.add("bi-eye-slash-fill");

        }else{

            senhaInput.type = "password";
            icon.classList.remove("bi-eye-slash-fill");
            icon.classList.add("bi-eye-fill");

        }

    });

}