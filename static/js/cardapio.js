// =====================================================
// CARDAPIO.JS
// Café Lumière
// =====================================================

let carrinho = [];

// =====================================================
// CARREGAMENTO
// =====================================================

document.addEventListener("DOMContentLoaded", () => {

    carregarCarrinho();
    atualizarCarrinho();

});

// =====================================================
// ADICIONAR PRODUTO
// =====================================================

function adicionarProduto(nome, preco){

    const produtoExistente = carrinho.find(
        item => item.nome === nome
    );

    if(produtoExistente){

        produtoExistente.quantidade++;

    }else{

        carrinho.push({
            nome: nome,
            preco: preco,
            quantidade: 1
        });

    }

    salvarCarrinho();
    atualizarCarrinho();

}

// =====================================================
// REMOVER PRODUTO
// =====================================================

function removerProduto(nome){

    const produto = carrinho.find(
        item => item.nome === nome
    );

    if(!produto) return;

    produto.quantidade--;

    if(produto.quantidade <= 0){

        carrinho = carrinho.filter(
            item => item.nome !== nome
        );

    }

    salvarCarrinho();
    atualizarCarrinho();

}

// =====================================================
// ATUALIZAR CARRINHO
// =====================================================

function atualizarCarrinho(){

    const lista = document.getElementById("lista");
    const total = document.getElementById("total");

    if(!lista || !total) return;

    lista.innerHTML = "";

    let valorTotal = 0;

    carrinho.forEach(produto => {

        const subtotal =
            produto.preco * produto.quantidade;

        valorTotal += subtotal;

        const li = document.createElement("li");

        li.innerHTML = `
            <strong>${produto.nome}</strong><br>
            ${produto.quantidade}x
            R$ ${produto.preco.toFixed(2)}
            <br>
            Subtotal:
            R$ ${subtotal.toFixed(2)}
        `;

        lista.appendChild(li);

    });

    total.innerText =
        valorTotal.toFixed(2);

}

// =====================================================
// SALVAR CARRINHO
// =====================================================

function salvarCarrinho(){

    localStorage.setItem(
        "carrinho",
        JSON.stringify(carrinho)
    );

}

// =====================================================
// CARREGAR CARRINHO
// =====================================================

function carregarCarrinho(){

    const dados =
        localStorage.getItem("carrinho");

    if(dados){

        carrinho = JSON.parse(dados);

    }

}

// =====================================================
// LIMPAR CARRINHO
// =====================================================

function limparCarrinho(){

    if(carrinho.length === 0){

        alert("Carrinho vazio.");
        return;

    }

    if(confirm("Deseja limpar o carrinho?")){

        carrinho = [];

        salvarCarrinho();
        atualizarCarrinho();

    }

}

// =====================================================
// FINALIZAR PEDIDO
// =====================================================

function finalizarPedido(){

    if(carrinho.length === 0){

        alert("Adicione produtos ao carrinho.");
        return;

    }

    let total = 0;

    carrinho.forEach(produto => {

        total +=
        produto.preco *
        produto.quantidade;

    });

    alert(
        "Pedido realizado com sucesso!\n\n" +
        "Total: R$ " +
        total.toFixed(2)
    );

    carrinho = [];

    salvarCarrinho();
    atualizarCarrinho();

}

// =====================================================
// PESQUISA DE PRODUTOS
// =====================================================

function pesquisarProdutos(){

    const busca =
        document.getElementById("busca");

    if(!busca) return;

    const texto =
        busca.value.toLowerCase();

    const produtos =
        document.querySelectorAll(".item");

    produtos.forEach(produto => {

        const nome =
        produto.innerText.toLowerCase();

        if(nome.includes(texto)){

            produto.style.display = "block";

        }else{

            produto.style.display = "none";

        }

    });

}

// =====================================================
// FILTRAR CATEGORIA
// =====================================================

function filtrarCategoria(categoria){

    const categorias =
        document.querySelectorAll(".categoria");

    categorias.forEach(secao => {

        if(
            categoria === "todos" ||
            secao.dataset.categoria === categoria
        ){

            secao.style.display = "block";

        }else{

            secao.style.display = "none";

        }

    });

}
// =====================================================
// ALTERAR QUANTIDADE
// =====================================================

function alterarQuantidade(botao, valor, nome, preco){

    if(valor > 0){

        adicionarProduto(nome, preco);

    }else{

        removerProduto(nome);

    }

    let qtdElemento =
        botao.parentElement.querySelector(".qtd");

    let quantidadeAtual =
        parseInt(qtdElemento.innerText);

    quantidadeAtual += valor;

    if(quantidadeAtual < 0){
        quantidadeAtual = 0;
    }

    qtdElemento.innerText = quantidadeAtual;

}

// =====================================================
// MODAL
// =====================================================

function abrirModal(){

    document
    .getElementById("modal")
    .style.display = "flex";

}

function fecharModal(){

    document
    .getElementById("modal")
    .style.display = "none";

}

// =====================================================
// WHATSAPP
// =====================================================

function enviarWhatsApp(){

    let total =
    document.getElementById("total")
    .innerText;

    let mensagem =
    "Olá! Gostaria de fazer este pedido:%0A%0A";

    carrinho.forEach(produto => {

        mensagem +=
        produto.quantidade +
        "x " +
        produto.nome +
        "%0A";

    });

    mensagem += "%0ATotal: R$ " + total;

    window.open(
        "https://wa.me/5547999999999?text=" +
        mensagem,
        "_blank"
    );

}