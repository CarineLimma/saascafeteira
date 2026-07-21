// =========================================
// DASHBOARD - INICIALIZAÇÃO
// =========================================

document.addEventListener("DOMContentLoaded", () => {
  animarValores();
  inicializarGrafico();
});

// =========================================
// ANIMAÇÃO DE VALORES (efeito contador)
// =========================================
function animarValores() {
  const valores = document.querySelectorAll(".card p");

  valores.forEach((el) => {
    let valorFinal = parseFloat(el.innerText.replace(/[^\d.-]/g, "")) || 0;
    let atual = 0;
    let incremento = valorFinal / 60;

    let contador = setInterval(() => {
      atual += incremento;

      if (atual >= valorFinal) {
        atual = valorFinal;
        clearInterval(contador);
      }

      el.innerText = formatarValor(atual);
    }, 15);
  });
}

// =========================================
// FORMATAÇÃO DE VALORES (R$)
// =========================================
function formatarValor(valor) {
  return valor.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
}

// =========================================
// GRÁFICO (Chart.js)
// =========================================
function inicializarGrafico() {
  const canvas = document.getElementById("graficoFinanceiro");

  if (!canvas) return;

  const ctx = canvas.getContext("2d");

  // Dados vindos do backend (Flask pode injetar via Jinja)
  const dadosEntradas = window.entradas || [1200, 1900, 3000, 2500, 3200];
  const dadosSaidas = window.saidas || [800, 1200, 1500, 1000, 1800];

  new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Jan", "Fev", "Mar", "Abr", "Mai"],
      datasets: [
        {
          label: "Entradas",
          data: dadosEntradas,
          borderColor: "#00d084",
          backgroundColor: "rgba(0, 208, 132, 0.1)",
          tension: 0.4,
          fill: true,
        },
        {
          label: "Saídas",
          data: dadosSaidas,
          borderColor: "#ff4d4d",
          backgroundColor: "rgba(255, 77, 77, 0.1)",
          tension: 0.4,
          fill: true,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          labels: {
            color: "#fff",
          },
        },
      },
      scales: {
        x: {
          ticks: { color: "#ccc" },
          grid: { color: "rgba(255,255,255,0.05)" },
        },
        y: {
          ticks: { color: "#ccc" },
          grid: { color: "rgba(255,255,255,0.05)" },
        },
      },
    },
  });
}

// =========================================
// ATUALIZAÇÃO DINÂMICA (opcional)
// =========================================
function atualizarDashboard(entradas, saidas) {
  window.entradas = entradas;
  window.saidas = saidas;

  inicializarGrafico();
}