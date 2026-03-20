const API_URL = "http://127.0.0.1:5000/classify_image";

const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const classifyBtn = document.getElementById("classifyBtn");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");

let selectedImageBase64 = "";

function setStatus(message) {
    statusEl.textContent = message;
}

imageInput.addEventListener("change", () => {
    const file = imageInput.files && imageInput.files[0];
    selectedImageBase64 = "";
    resultEl.textContent = "";

    if (!file) {
        preview.classList.add("hidden");
        preview.removeAttribute("src");
        setStatus("");
        return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
        const dataUrl = String(event.target.result || "");
        preview.src = dataUrl;
        preview.classList.remove("hidden");

        const splitIndex = dataUrl.indexOf(",");
        selectedImageBase64 = splitIndex >= 0 ? dataUrl.slice(splitIndex + 1) : dataUrl;
        setStatus("Image loaded.");
    };
    reader.onerror = () => {
        setStatus("Could not read file.");
    };
    reader.readAsDataURL(file);
});

classifyBtn.addEventListener("click", async () => {
    if (!selectedImageBase64) {
        setStatus("Please choose an image first.");
        return;
    }

    classifyBtn.disabled = true;
    setStatus("Classifying...");
    resultEl.textContent = "";

    try {
        const formData = new FormData();
        formData.append("image_base64", selectedImageBase64);

        const response = await fetch(API_URL, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const data = await response.json();

        if (!Array.isArray(data) || data.length === 0) {
            setStatus("No face was detected. Try another image.");
            return;
        }

        setStatus("Done.");
        
        // Format results nicely
        resultEl.innerHTML = data.map((result, idx) => {
            const percentage = Math.round(result.class_probability * 100);
            const confidenceLevel = percentage === 100 ? "Very High" : 
                                   percentage >= 80 ? "High" : 
                                   percentage >= 60 ? "Medium" : "Low";
            
            return `
                <div class="result-card">
                    <div class="face-number">Face ${idx + 1}</div>
                    <div class="celeb-name">${result.class}</div>
                    <div class="confidence-container">
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: ${percentage}%"></div>
                        </div>
                        <div class="confidence-text">
                            <span class="percentage">${percentage}%</span>
                            <span class="level">${confidenceLevel}</span>
                        </div>
                    </div>
                </div>
            `;
        }).join("");

    } catch (error) {
        setStatus("Request failed. Make sure the backend server is running.");
        resultEl.textContent = String(error);
    } finally {
        classifyBtn.disabled = false;
    }
});
