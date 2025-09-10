async function checkHeadline() {
    const query = document.getElementById('headline').value;
    const resultsDiv = document.getElementById('results');

    if (!query.trim()) {
        resultsDiv.innerHTML = "<p style='color:orange;'>Please enter a headline.</p>";
        return;
    }

    resultsDiv.innerHTML = "<p>Loading news...</p>";

    try {
        // Replace with your own API key from https://newsapi.org
        const API_KEY = "3807b27da8cf49e586ce3d3cc1f58fca";

        const res = await fetch(
            `https://newsapi.org/v2/everything?q=${encodeURIComponent(query)}&pageSize=5&sortBy=publishedAt&language=en&apiKey=${API_KEY}`
        );

        const data = await res.json();

        if (data.status !== "ok") {
            resultsDiv.innerHTML = `<p style="color:red;">Error: ${data.message}</p>`;
            return;
        }

        if (!data.articles || data.articles.length === 0) {
            resultsDiv.innerHTML = "<p>No news found for this headline.</p>";
            return;
        }

        // Show articles line by line
        resultsDiv.innerHTML = "";
        data.articles.forEach(article => {
            const div = document.createElement("div");
            div.classList.add("article");
            div.innerHTML = `
                <a href="${article.url}" target="_blank"><b>${article.title}</b></a><br>
                <small>${article.source.name} — ${new Date(article.publishedAt).toLocaleString()}</small>
                <p>${article.description || ""}</p>
                <hr>
            `;
            resultsDiv.appendChild(div);
        });
    } catch (err) {
        resultsDiv.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
    }
}
