console.log("Dashboard JS loaded");

const trustChart = document.getElementById("trustChart");

if (trustChart && typeof Chart !== "undefined") {
    new Chart(trustChart, {
        type: "bar",
        data: {
            labels: ["Radar", "RF", "EO/IR"],
            datasets: [{
                label: "Trust Score (%)",
                data: [94, 89, 91],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: "Trust (%)"
                    }
                }
            }
        }
    });
}