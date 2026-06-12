// 1. Procuramos o formulário na tela pelo ID que dei a ele no HTML
const formulario = document.getElementById('formCadastro');
const divMensagem = document.getElementById('mensagem-alerta');

// 2. Ficar esperando o momento exato em que o usuário clicar no botão de Submit
formulario.addEventListener('submit', async function(evento) {
    
    // 3. Isso impede que a página dê um "F5" (recarregue) sozinha quando clica no botão
    evento.preventDefault();

    // 4. Pegar o texto exato que o usuário digitou dentro de cada caixinha
    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    const telefone = document.getElementById('telefone').value;
    const senha = document.getElementById('senha').value;

    // 5. Montar o "pacote" (JSON) com as etiquetas que o nosso Python está esperando
    const dadosParaEnviar = {
        nome: nome,
        email: email,
        telefone: telefone,
        senha: senha
    };

    try {
        // 6. Chamar o motoboy (Fetch). Ele vai levar o pacote até a rota do Flask
        const resposta = await fetch('/api/cadastro', {
            method: 'POST', // POST significa "Estou te enviando dados para salvar"
            headers: {
                'Content-Type': 'application/json' // Avisa que o pacote é um JSON
            },
            body: JSON.stringify(dadosParaEnviar) // Transforma nosso pacote em texto para viajar pela internet
        });

        // 7. O Python processou e nos devolveu uma resposta. Vamos ler o que ele disse:
        const dadosResposta = await resposta.json();

        // 8. Se o código for 200 ou 201 (Sucesso absoluto, o código do HTML)
        if (resposta.ok) {
            divMensagem.textContent = "Sucesso: " + dadosResposta.mensagem;
            divMensagem.style.display = "block";
            divMensagem.style.color = "green";
            divMensagem.style.marginBottom = "15px";
            
            // Limpa as caixinhas de digitar depois de cadastrar
            formulario.reset(); 
        } 
        // 9. Se o Python devolveu um erro (ex: email já cadastrado)
        else {
            divMensagem.textContent = "Erro: " + dadosResposta.erro;
            divMensagem.style.display = "block";
            divMensagem.style.color = "red";
            divMensagem.style.marginBottom = "15px";
        }

    } catch (erro) {
        // 10. Se a internet do usuário cair ou o servidor Python estiver desligado
        divMensagem.textContent = "Erro de conexão com o servidor.";
        divMensagem.style.display = "block";
        divMensagem.style.color = "red";
        divMensagem.style.marginBottom = "15px";
    }
});