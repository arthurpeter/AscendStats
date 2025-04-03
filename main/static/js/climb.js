document.addEventListener('DOMContentLoaded', function() {
    // Edit modal logic
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', function() {
            const climbId = this.dataset.climbId;
            const editForm = document.getElementById('editClimbForm');
            
            // Set form action URL
            editForm.action = `/climb/edit/${climbId}/`;
            
            // Populate fields using NAME attributes (not IDs)
            const fields = {
                'grade': this.dataset.grade,
                'success': this.dataset.success === 'True',
                'attempts': this.dataset.attempts,
                'style': this.dataset.style,
                'notes': this.dataset.notes
            };
    
            Object.entries(fields).forEach(([name, value]) => {
                const input = editForm.querySelector(`[name="${name}"]`);
                if (input.type === 'checkbox') {
                    input.checked = value;
                } else {
                    input.value = value;
                }
            });
        });
    });

    // Show the edit modal if editing
    if (window.editing) {
        const editModal = new bootstrap.Modal(document.getElementById('editClimbModal'));
        editModal.show();
    }

});


