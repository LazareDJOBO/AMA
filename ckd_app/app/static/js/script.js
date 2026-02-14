document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const resultSection = document.getElementById('result-section');
    const loader = document.getElementById('loader');
    const btnText = document.querySelector('.btn-text');
    let probabilityChart = null;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // UI Updates
        loader.style.display = 'inline-block';
        btnText.textContent = 'Analyse en cours...';
        resultSection.classList.add('hidden');

        // Gather Data
        const formData = {
            age: parseInt(document.getElementById('age').value),
            sexe: document.getElementById('sexe').value,
            creatinine: parseFloat(document.getElementById('creatinine').value),
            uree: parseFloat(document.getElementById('uree').value),
            temperature: parseFloat(document.getElementById('temperature').value),
            cholesterol_ldl: document.getElementById('cholesterol_ldl').value,
            cholesterol_total: document.getElementById('cholesterol_total').value
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Erreur lors de la prédiction');
            }

            const result = await response.json();
            displayResults(result);

        } catch (error) {
            alert('Erreur: ' + error.message);
        } finally {
            loader.style.display = 'none';
            btnText.textContent = "Lancer l'analyse";
        }
    });

    function displayResults(data) {
        // Show section
        resultSection.classList.remove('hidden');
        resultSection.scrollIntoView({ behavior: 'smooth' });

        // Update Stage
        const stageEl = document.getElementById('predicted-stage');
        stageEl.textContent = `Stade ${data.stage}`;
        
        // Update Description
        const descriptions = {
            0: "Absence de maladie rénale ou stade très précoce.",
            1: "Stade 1 : Maladie rénale chronique avec fonction rénale normale.",
            2: "Stade 2 : Maladie rénale chronique avec perte légère de fonction.",
            3: "Stade 3 : Perte modérée de la fonction rénale.",
            4: "Stade 4 : Perte sévère de la fonction rénale.",
            5: "Stade 5 : Insuffisance rénale terminale."
        };
        document.getElementById('stage-description').textContent = descriptions[data.stage] || "Résultat obtenu.";

        // Update Chart
        updateChart(data.probabilities);
    }

    function updateChart(probabilities) {
        const ctx = document.getElementById('probabilityChart').getContext('2d');
        
        // Prepare data sorted by stage
        const labels = Object.keys(probabilities).sort().map(k => `Stade ${k}`);
        const data = Object.keys(probabilities).sort().map(k => probabilities[k]);

        if (probabilityChart) {
            probabilityChart.destroy();
        }

        probabilityChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Probabilité',
                    data: data,
                    backgroundColor: 'rgba(0, 123, 255, 0.6)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Probabilités par Stade'
                    }
                }
            }
        });
    }
});
