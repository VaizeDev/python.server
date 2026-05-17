const result = document.getElementById("result");

document.getElementById("timeButton").addEventListener("click", async () => {
    const response = await fetch("/api/time");
    const data = await response.json();

    result.textContent = JSON.stringify(data, null, 2);
});

document.getElementById("greetButton").addEventListener("click", async () => {
    const name = document.getElementById("nameInput").value;

    const response = await fetch("/api/greet", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name
        })
    });

    const data = await response.json();

    result.textContent = JSON.stringify(data, null, 2);
});