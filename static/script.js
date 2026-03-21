// currently selected analysis type (default is news)
let selectedType = "news";

// handle type selector buttons
const typeButtons = document.querySelectorAll(".type-btn");
typeButtons.forEach(function(btn) {
    btn.addEventListener("click", function() {
        // remove active from all buttons first
        typeButtons.forEach(function(b) {
            b.classList.remove("active");
        });
        // set clicked button as active
        btn.classList.add("active");
        selectedType = btn.dataset.type;
    });
});


// fetch and display dashboard stats
async function loadStats() {
    try {
        const response = await fetch("/api/stats");
        const stats = await response.json();

        document.getElementById("totalScans").textContent = stats.total_scans;
        document.getElementById("threatsDetected").textContent = stats.threats_detected;
        document.getElementById("safeContent").textContent = stats.safe_content;
        document.getElementById("threatRate").textContent = stats.threat_rate + "%";
    } catch (error) {
        console.log("Could not load stats:", error);
    }
}


// fetch and display scan history
async function loadHistory() {
    try {
        const response = await fetch("/api/history?limit=10");
        const scans = await response.json();
        const historyList = document.getElementById("historyList");

        if (scans.length === 0) {
            historyList.innerHTML = '<p class="empty-state">No scans yet. Try scanning some content above!</p>';
            return;
        }

        // build history items HTML
        let html = "";
        for (let i = 0; i < scans.length; i++) {
            const scan = scans[i];
            const verdictClass = scan.verdict.toLowerCase();
            const time = new Date(scan.created_at).toLocaleString();

            // truncate long text
            let displayText = scan.input_text;
            if (displayText.length > 80) {
                displayText = displayText.substring(0, 80) + "...";
            }

            html += `
            <div class="history-item">
                <span class="history-verdict ${verdictClass}">${scan.verdict}</span>
                <span class="history-text">${escapeHtml(displayText)}</span>
                <span class="history-meta">${time}</span>
            </div>`;
        }

        historyList.innerHTML = html;
    } catch (error) {
        console.log("Could not load history:", error);
    }
}


// main scan function - called when user clicks "Scan Now"
async function scanText() {
    const inputField = document.getElementById("inputText");
    const text = inputField.value.trim();

    // don't scan empty text
    if (!text) {
        inputField.focus();
        return;
    }

    // show loading state on button
    const scanBtn = document.getElementById("scanBtn");
    const btnText = scanBtn.querySelector(".btn-text");
    const btnLoading = scanBtn.querySelector(".btn-loading");

    scanBtn.disabled = true;
    btnText.style.display = "none";
    btnLoading.style.display = "inline";

    try {
        // send POST request to our backend API
        const response = await fetch("/api/scan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text: text,
                analysis_type: selectedType
            }),
        });

        const data = await response.json();

        // show the result and refresh stats + history
        displayResult(data);
        loadStats();
        loadHistory();

    } catch (error) {
        alert("Error: Could not connect to the server. Make sure it's running!");
        console.error(error);
    } finally {
        // reset button state
        scanBtn.disabled = false;
        btnText.style.display = "inline";
        btnLoading.style.display = "none";
    }
}


// display the scan result on the page
function displayResult(data) {
    const resultCard = document.getElementById("resultCard");
    const header = document.getElementById("resultHeader");
    const badge = document.getElementById("verdictBadge");
    const confidenceFill = document.getElementById("confidenceFill");
    const confidenceValue = document.getElementById("confidenceValue");
    const explanation = document.getElementById("explanation");
    const riskDiv = document.getElementById("riskIndicators");
    const riskList = document.getElementById("riskList");

    // set the color theme based on verdict
    const verdictLower = data.verdict.toLowerCase();
    header.className = "result-header " + verdictLower;

    // set verdict text
    badge.textContent = data.verdict;

    // set confidence percentage and bar width
    const percentage = Math.round(data.confidence_score * 100);
    confidenceFill.style.width = percentage + "%";
    confidenceValue.textContent = percentage + "%";

    // change bar color based on verdict type
    if (data.verdict === "FAKE" || data.verdict === "SCAM") {
        confidenceFill.style.background = "var(--danger)";
    } else if (data.verdict === "REAL" || data.verdict === "SAFE") {
        confidenceFill.style.background = "var(--success)";
    } else {
        confidenceFill.style.background = "var(--warning)";
    }

    // show the explanation
    explanation.textContent = data.explanation;

    // show risk indicators if available
    if (data.risk_indicators) {
        try {
            const risks = JSON.parse(data.risk_indicators);
            if (risks.length > 0) {
                let risksHtml = "";
                for (let i = 0; i < risks.length; i++) {
                    risksHtml += "<li>" + escapeHtml(risks[i]) + "</li>";
                }
                riskList.innerHTML = risksHtml;
                riskDiv.style.display = "block";
            } else {
                riskDiv.style.display = "none";
            }
        } catch (e) {
            riskDiv.style.display = "none";
        }
    } else {
        riskDiv.style.display = "none";
    }

    // show the result card with smooth scroll
    resultCard.style.display = "block";
    resultCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
}


// helper function to prevent XSS attacks
function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}


// keyboard shortcut: Ctrl+Enter to scan
document.getElementById("inputText").addEventListener("keydown", function(e) {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
        scanText();
    }
});


// load data when page first opens
loadStats();
loadHistory();
