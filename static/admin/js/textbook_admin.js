document.addEventListener('DOMContentLoaded', function() {
    const subjectField = document.querySelector('#id_subject');
    const sectionField = document.querySelector('#id_section');
    
    if (subjectField && sectionField) {
        // Subject o'zgarganda section larni yangilash
        subjectField.addEventListener('change', function() {
            const subjectId = this.value;
            
            // Section field ni tozalash
            sectionField.innerHTML = '<option value="">---------</option>';
            
            if (subjectId) {
                // AJAX orqali section larni olish
                fetch(`/admin/get-sections/${subjectId}/`)
                    .then(response => response.json())
                    .then(data => {
                        data.sections.forEach(section => {
                            const option = document.createElement('option');
                            option.value = section.id;
                            option.textContent = section.name;
                            sectionField.appendChild(option);
                        });
                    })
                    .catch(error => {
                        console.error('Qismlarni yuklashda xatolik:', error);
                    });
            }
        });
        
        // Sahifa yuklanganda agar subject tanlangan bo'lsa, section larni yuklash
        if (subjectField.value) {
            subjectField.dispatchEvent(new Event('change'));
        }
    }
});
