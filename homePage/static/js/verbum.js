// ocultar senha 

const password = document.querySelector("#password");
const togglePassword = document.querySelector("#toggle-password");

if (password && togglePassword) {
  // Informações utilizadas por leitores de tela
  togglePassword.setAttribute("aria-controls", "password");
  togglePassword.setAttribute("aria-pressed", "false");
  togglePassword.setAttribute("aria-label", "Mostrar senha");

  togglePassword.addEventListener("click", () => {
    const passwordIsHidden = password.type === "password";

    password.type = passwordIsHidden ? "text" : "password";
    togglePassword.textContent = passwordIsHidden
      ? "Ocultar"
      : "Mostrar";

    togglePassword.setAttribute(
      "aria-pressed",
      String(passwordIsHidden)
    );

    togglePassword.setAttribute(
      "aria-label",
      passwordIsHidden
        ? "Ocultar senha"
        : "Mostrar senha"
    );

    // Retorna o foco para o campo de senha
    password.focus();
  });
}

// confirmar senha no cadastro

const passwordConfirmation = document.querySelector(
  "#password_confirmation"
);

if (password && passwordConfirmation) {
  function validatePasswordConfirmation() {
    const passwordsAreEqual =
      password.value === passwordConfirmation.value;

    if (
      passwordConfirmation.value !== "" &&
      !passwordsAreEqual
    ) {
      passwordConfirmation.setCustomValidity(
        "As senhas não coincidem."
      );
    } else {
      passwordConfirmation.setCustomValidity("");
    }
  }

  password.addEventListener(
    "input",
    validatePasswordConfirmation
  );

  passwordConfirmation.addEventListener(
    "input",
    validatePasswordConfirmation
  );
}

// evita envios repetidos

const forms = document.querySelectorAll("form");

forms.forEach((form) => {
  form.addEventListener("submit", () => {
    // Só continua se os campos estiverem válidos
    if (!form.checkValidity()) {
      return;
    }

    const submitButton = form.querySelector(
      'button[type="submit"]'
    );

    if (!submitButton) {
      return;
    }

    // Impede que o usuário envie o formulário várias vezes
    submitButton.disabled = true;
    submitButton.setAttribute("aria-busy", "true");

    if (submitButton.classList.contains("button-primary")) {
      submitButton.textContent = "Entrando...";
    } else if (
      submitButton.classList.contains("register-button")
    ) {
      submitButton.textContent = "Cadastrando...";
    } else {
      submitButton.textContent = "Enviando...";
    }
  });
});


// botao para iniciar uma atividade

const startLesson = document.querySelector("#start-lesson");

if (startLesson) {
  startLesson.setAttribute("aria-pressed", "false");

  startLesson.addEventListener("click", () => {
    startLesson.textContent = "Atividade selecionada ✓";
    startLesson.classList.add("selected");
    startLesson.setAttribute("aria-pressed", "true");
  });
}

const logoutButton = document.getElementById("logoutButton");
const logoutModal = document.getElementById("logoutModal");
const cancelLogout = document.getElementById("cancelLogout");

if (logoutButton && logoutModal && cancelLogout) {

    logoutButton.addEventListener("click", function(event) {
        event.preventDefault();
        logoutModal.classList.add("active");
    });

    cancelLogout.addEventListener("click", function() {
        logoutModal.classList.remove("active");
    });

    logoutModal.addEventListener("click", function(event) {
        if (event.target === logoutModal) {
            logoutModal.classList.remove("active");
        }
    });

}