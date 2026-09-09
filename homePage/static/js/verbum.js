// MOSTRAR OU OCULTAR A SENHA

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

// CONFIRMAÇÃO DA SENHA NO CADASTRO

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

// EVITAR VÁRIOS ENVIOS DO MESMO FORMULÁRIO

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


// BOTÃO PARA INICIAR UMA ATIVIDADE

const startLesson = document.querySelector("#start-lesson");

if (startLesson) {
  startLesson.setAttribute("aria-pressed", "false");

  startLesson.addEventListener("click", () => {
    startLesson.textContent = "Atividade selecionada ✓";
    startLesson.classList.add("selected");
    startLesson.setAttribute("aria-pressed", "true");
  });
}