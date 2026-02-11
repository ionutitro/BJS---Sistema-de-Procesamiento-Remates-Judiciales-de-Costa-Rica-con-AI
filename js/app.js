const API_URL = "http://localhost:8000/api";

document.addEventListener('DOMContentLoaded', () => {
    loadRemates();

    document.getElementById('uploadForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const fileInput = document.getElementById('pdfFile');
        const file = fileInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${API_URL}/upload`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                alert('Archivo subido y enviado a procesar. Recargue en unos momentos.');
                fileInput.value = '';
                loadRemates();
            } else {
                alert('Error al subir el archivo');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error de conexión');
        }
    });
});

async function loadRemates() {
    try {
        const response = await fetch(`${API_URL}/remates`);
        const data = await response.json();
        const tbody = document.getElementById('rematesTableBody');
        tbody.innerHTML = '';

        data.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${item.id}</td>
                <td><span class="badge ${item.tipo === 'vehiculo' ? 'bg-info' : 'bg-warning'}">${item.tipo}</span></td>
                <td>${item.descripcion ? item.descripcion.substring(0, 50) + '...' : ''}</td>
                <td>${item.precio_base || 'N/A'}</td>
                <td>${item.ubicacion || 'N/A'}</td>
                <td>${item.fecha_remate || 'N/A'}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="showDetails(${item.id})">Ver Detalles</button>
                    <button class="btn btn-sm btn-danger ms-2" onclick="deleteRemate(${item.id})">Borrar</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

async function deleteRemate(id) {
    if (!confirm('¿Está seguro de que desea eliminar este remate?')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/remates/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            alert('Remate eliminado correctamente');
            loadRemates(); // Refresh the list
        } else {
            alert('Error al eliminar el remate');
        }
    } catch (error) {
        console.error('Error deleting remate:', error);
        alert('Error de conexión al eliminar');
    }
}

async function showDetails(id) {
    // Ideally fetch full details if not already loaded, but we can reuse if we had full list
    // OR fetch specifically
    try {
        const response = await fetch(`${API_URL}/remates/${id}`);
        const data = await response.json(); // returns array or object
        // The API returns a single object for /remates/{id} ? No, currently my main.py returns list for /remates and single for /remates/{id}
        // Let me check main.py... It has get_remate.

        const modalBody = document.getElementById('modalBody');
        modalBody.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <h6>Tipo</h6> <p>${data.tipo}</p>
                    <h6>Marca/Modelo</h6> <p>${data.marca || '-'} / ${data.modelo || '-'}</p>
                    <h6>Placa/Matrícula</h6> <p>${data.placa || data.matricula || '-'}</p>
                    <h6>VIN</h6> <p>${data.vin || '-'}</p>
                </div>
                <div class="col-md-6">
                    <h6>Precio Base</h6> <p>${data.precio_base}</p>
                    <h6>Fecha</h6> <p>${data.fecha_remate}</p>
                    <h6>Juzgado</h6> <p>${data.juzgado}</p>
                    <h6>Ubicación</h6> <p>${data.ubicacion}</p>
                </div>
            </div>
            <hr>
            <h6>Texto Completo</h6>
            <pre class="bg-light p-3" style="white-space: pre-wrap; max-height: 300px; overflow-y: auto;">${data.texto_completo}</pre>
        `;

        new bootstrap.Modal(document.getElementById('detailModal')).show();
    } catch (error) {
        console.error('Error fetching details:', error);
    }
}
