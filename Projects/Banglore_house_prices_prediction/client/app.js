// Load dropdown options when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadLocations();
    loadSocieties();
    loadAreaTypes();
});

async function loadLocations() {
    try {
        const response = await fetch(`/api/get_location_names`);
        const data = await response.json();
        const select = document.getElementById('location');
        
        data.locations.forEach(location => {
            const option = document.createElement('option');
            option.value = location;
            option.textContent = location;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading locations:', error);
        alert('Failed to load locations. Make sure the server is running.');
    }
}

async function loadSocieties() {
    try {
        const response = await fetch(`/api/get_society_names`);
        const data = await response.json();
        const select = document.getElementById('society');
        
        data.societies.forEach(society => {
            const option = document.createElement('option');
            option.value = society;
            option.textContent = society;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading societies:', error);
        alert('Failed to load societies. Make sure the server is running.');
    }
}

async function loadAreaTypes() {
    try {
        const response = await fetch(`/api/get_area_type_names`);
        const data = await response.json();
        const select = document.getElementById('area_type');
        
        data.area_types.forEach(area => {
            const option = document.createElement('option');
            option.value = area;
            option.textContent = area;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading area types:', error);
        alert('Failed to load area types. Make sure the server is running.');
    }
}

// Handle form submission
document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        location: document.getElementById('location').value,
        society: document.getElementById('society').value,
        area_type: document.getElementById('area_type').value,
        total_sqft: document.getElementById('total_sqft').value,
        bhk: document.getElementById('bhk').value,
        bath: document.getElementById('bath').value,
        balcony: document.getElementById('balcony').value
    };
    
    try {
        const response = await fetch(`/api/predict_home_price`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.estimated_price && data.estimated_price !== -1) {
            document.getElementById('price').textContent = `₹ ${data.estimated_price} Lakhs`;
            document.getElementById('result').classList.remove('hidden');
        } else {
            alert('Unable to predict price. Please check your inputs.');
        }
    } catch (error) {
        console.error('Error making prediction:', error);
        alert('Failed to get prediction. Make sure the server is running.');
    }
});