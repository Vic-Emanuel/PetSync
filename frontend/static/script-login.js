// 1. Procuramos o formulário de login e a caixa de mensagens na tela
const formLogin = document.getElementById('formLogin');
const divMensagem = document.getElementById('mensagem-alerta');

// 2. Escutamos o clique no botão "Entrar"
formLogin.addEventListener('submit', async function(evento) {
    
    // 3. Impede a página de recarregar
    evento.preventDefault();

    // 4. Pega o e-mail e a senha que o tutor digitou
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;

    // 5. Monta o pacote JSON
    const dadosLogin = {
        email: email,
        senha: senha
    };

    try {
        // 6. Envia o pacote para a nossa nova rota do Blueprint no Flask
        const resposta = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dadosLogin)
        });

        const dadosResposta = await resposta.json();

        // 7. Se a senha e o e-mail estiverem corretos (Status 200)
        if (resposta.ok) {
            divMensagem.textContent = "Sucesso: " + dadosResposta.mensagem;
            divMensagem.style.display = "block";
            divMensagem.style.color = "green";
            divMensagem.style.marginBottom = "15px";
            
            // Opcional: Limpa o formulário após o login
            formLogin.reset(); 

            // Nota de Engenharia: No futuro, é aqui que usaremos o comando 
            // window.location.href = "/dashboard" para redirecionar o usuário!
            
        } 
        // 8. Se a senha ou e-mail estiverem errados (O Greatshield bloqueou - Status 401)
        else {
            divMensagem.textContent = "Erro: " + dadosResposta.erro;
            divMensagem.style.display = "block";
            divMensagem.style.color = "red";
            divMensagem.style.marginBottom = "15px";
        }

    } catch (erro) {
        // 9. Se o servidor Flask estiver desligado
        divMensagem.textContent = "Erro de conexão com o servidor.";
        divMensagem.style.display = "block";
        divMensagem.style.color = "red";
        divMensagem.style.marginBottom = "15px";
    }
});