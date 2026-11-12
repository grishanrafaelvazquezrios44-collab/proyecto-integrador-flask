document.addEventListener("DOMContentLoaded", function () {

    const formularios = document.querySelectorAll("form");

    formularios.forEach(function(formulario) {

        formulario.addEventListener("submit", function(evento) {

            const campos = formulario.querySelectorAll("[required]");

            for (let campo of campos) {
                if (campo.value.trim() === "") {
                    evento.preventDefault();
                    alert("Por favor, completa todos los campos.");
                    campo.focus();
                    return;
                }
            }

            const boletos = formulario.querySelector('[name="boletos"]');

            if (boletos) {
                if (boletos.value < 1 || boletos.value > 10) {
                    evento.preventDefault();
                    alert("Selecciona entre 1 y 10 boletos.");
                    boletos.focus();
                }
            }

        });

    });

});
