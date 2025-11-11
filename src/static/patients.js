document.addEventListener('DOMContentLoaded', function () {
  const liveSearch = document.getElementById('liveSearch');
  const table = document.getElementById('patientsTable');
  const tbody = table && table.querySelector('tbody');
  const cardToggle = document.getElementById('cardToggle');

  if (!table || !tbody) return;

  // Live filter across visible columns
  function filterRows(term) {
    term = (term || '').trim().toLowerCase();
    const rows = Array.from(tbody.querySelectorAll('tr.main-row'));
    rows.forEach(main => {
      const details = main.nextElementSibling; // details-row
      const text = (main.textContent + ' ' + (details ? details.textContent : '')).toLowerCase();
      const match = term === '' || text.indexOf(term) !== -1;
      main.style.display = match ? '' : 'none';
      if (details) details.style.display = match ? '' : 'none';
    });
  }

  if (liveSearch) {
    liveSearch.addEventListener('input', function (e) {
      filterRows(e.target.value);
    });
  }

  // Toggle details rows when clicking Details button
  tbody.addEventListener('click', function (e) {
    const btn = e.target.closest('.details-btn');
    if (!btn) return;
    const main = btn.closest('tr.main-row');
    if (!main) return;
    const details = main.nextElementSibling;
    if (!details) return;
    const visible = details.style.display !== 'none' && details.style.display !== '';
    // Toggle display; default is none from CSS
    if (visible) {
      details.style.display = 'none';
    } else {
      details.style.display = '';
      // optionally scroll into view for small screens
      if (window.innerWidth < 900) {
        details.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  });

  // Card view toggle
  if (cardToggle) {
    cardToggle.addEventListener('change', function (e) {
      const container = document.getElementById('patientsContainer');
      if (!container) return;
      if (e.target.checked) {
        container.classList.add('card-view');
        document.body.classList.add('card-view');
      } else {
        container.classList.remove('card-view');
        document.body.classList.remove('card-view');
      }
    });
  }

  // Sorting: click on th with data-sort
  const headers = Array.from(table.querySelectorAll('th[data-sort]'));
  headers.forEach((th, index) => {
    th.style.cursor = 'pointer';
    th.addEventListener('click', function () {
      const type = th.getAttribute('data-sort') || 'string';
      sortTableByColumn(index, type);
      // Toggle sort indicator (simple)
      headers.forEach(h => h.classList.remove('sort-asc', 'sort-desc'));
      const currentClass = th.classList.contains('sort-asc') ? 'sort-desc' : 'sort-asc';
      th.classList.add(currentClass);
    });
  });

  function getCellValue(row, idx) {
    const cell = row.querySelectorAll('td')[idx];
    return cell ? cell.textContent.trim() : '';
  }

  function parseValue(val, type) {
    if (!val) return '';
    if (type === 'number') {
      const n = parseFloat(val.replace(/[^0-9.-]+/g, ''));
      return isNaN(n) ? 0 : n;
    }
    if (type === 'date') {
      const d = Date.parse(val);
      return isNaN(d) ? 0 : d;
    }
    return val.toString().toLowerCase();
  }

  function sortTableByColumn(colIdx, type) {
    const rows = Array.from(tbody.querySelectorAll('tr.main-row'));
    const pairs = rows.map(main => ({ main, details: main.nextElementSibling }));

    // Determine current direction by checking header class
    const th = headers.find((h, i) => i === Array.from(table.querySelectorAll('th[data-sort]')).indexOf(table.querySelectorAll('th')[colIdx]));

    pairs.sort((a, b) => {
      const aVal = parseValue(getCellValue(a.main, colIdx), type);
      const bVal = parseValue(getCellValue(b.main, colIdx), type);
      if (typeof aVal === 'string' && typeof bVal === 'string') return aVal.localeCompare(bVal);
      if (aVal < bVal) return -1;
      if (aVal > bVal) return 1;
      return 0;
    });

    // If header has sort-desc, reverse
    const header = Array.from(table.querySelectorAll('th'))[colIdx];
    const desc = header && header.classList && header.classList.contains('sort-desc');
    if (desc) pairs.reverse();

    // Re-append rows in sorted order
    pairs.forEach(p => {
      tbody.appendChild(p.main);
      if (p.details) tbody.appendChild(p.details);
    });
  }

  // initial filter to apply any current input value
  filterRows(liveSearch ? liveSearch.value : '');
});

// Modal handling for add/edit patient
document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('patientModal');
  const form = document.getElementById('patientForm');
  const modalTitle = document.getElementById('modalTitle');
  const cancelBtn = document.getElementById('cancelPatient');

  function showModal(mode, patientId, data) {
    if (!modal || !form) return;
    modal.style.display = '';
    if (mode === 'add') {
      modalTitle.textContent = 'Add Patient';
      form.action = '/patients/add';
      form.reset();
      const idField = form.querySelector('#patient_id'); if (idField) idField.value = '';
    } else if (mode === 'edit') {
      modalTitle.textContent = 'Edit Patient';
      form.action = `/patients/${patientId}/update`;
      // populate some common fields from provided data (partial)
      if (data) {
        ['first_name','last_name','date_of_birth','gender','blood_type','phone','email','address','emergency_contact','emergency_contact_phone','insurance_provider','insurance_number','primary_physician','next_appointment','allergies','past_medical_history'].forEach(k => {
          const el = form.querySelector(`#${k}`);
          if (el && data[k] !== undefined) el.value = data[k];
        });
      }
    }
  }

  function hideModal() {
    const modal = document.getElementById('patientModal');
    if (modal) modal.style.display = 'none';
  }

  // Add patient buttons (could be more than one per page)
  Array.from(document.querySelectorAll('#addPatientBtn')).forEach(btn => {
    btn.addEventListener('click', function () { showModal('add'); });
  });

  // Cancel button
  if (cancelBtn) cancelBtn.addEventListener('click', hideModal);

  // Edit buttons inside details rows
  document.addEventListener('click', function (e) {
    const edit = e.target.closest('.edit-btn');
    if (!edit) return;
    const id = edit.getAttribute('data-id');
    // find row and details
    const detailsRow = edit.closest('.details-grid');
    const mainRow = edit.closest('tr.details-row') ? edit.closest('tr.details-row').previousElementSibling : null;
    const data = {};
    if (mainRow) {
      const cells = mainRow.querySelectorAll('td');
      data.first_name = cells[1] ? cells[1].textContent.trim() : '';
      data.last_name = cells[2] ? cells[2].textContent.trim() : '';
      data.date_of_birth = cells[3] ? cells[3].textContent.trim() : '';
      data.gender = cells[4] ? cells[4].textContent.trim() : '';
      data.phone = cells[5] ? cells[5].textContent.trim() : '';
      data.email = cells[6] ? cells[6].textContent.trim() : '';
      data.primary_physician = cells[7] ? cells[7].textContent.trim() : '';
      data.next_appointment = cells[8] ? cells[8].textContent.trim() : '';
    }
    // try to extract some fields from details grid text nodes
    if (detailsRow) {
      Array.from(detailsRow.querySelectorAll('div')).forEach(div => {
        const text = div.textContent || '';
        if (text.startsWith('Address:')) data.address = text.replace('Address:', '').trim();
        if (text.startsWith('Emergency Contact:')) data.emergency_contact = text.replace('Emergency Contact:', '').split('—')[0].trim();
        if (text.startsWith('Insurance:')) data.insurance_provider = text.replace('Insurance:', '').split('(')[0].trim();
      });
    }
    showModal('edit', id, data);
  });

});
