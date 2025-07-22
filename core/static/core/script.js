const API_BASE = 'http://localhost:8000/api/';

document.getElementById('category-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('category-name').value;
    if (!name) { alert('Please provide a category name.'); return; }
    const res = await fetch(API_BASE + 'categories/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cat_name: name })
    });
    if (res.ok) {
        loadCategories();
        document.getElementById('category-name').value = '';
    }
});

async function loadCategories() {
    const res = await fetch(API_BASE + 'categories/');
    const data = await res.json();
    const list = document.getElementById('category-list');
    list.innerHTML = '';
    const catSelect = document.getElementById('account-category');
    catSelect.innerHTML = '';
    data.forEach(cat => {
        const li = document.createElement('li');
        li.textContent = cat.cat_name;
        document.getElementById('category-list').appendChild(li);

        const opt = document.createElement('option');
        opt.value = cat.cat_name;
        opt.textContent = cat.cat_name;
        catSelect.appendChild(opt);
    });
        const li = document.createElement('li');
        li.textContent = cat.cat_name;
        list.appendChild(li);
    });
}

document.getElementById('account-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('account-name').value;
    const category = document.getElementById('account-category').value;
    const notes = document.getElementById('account-notes').value;

    // Fetch category ID by name
    const catRes = await fetch(API_BASE + 'categories/');
    const cats = await catRes.json();
    const cat = cats.find(c => c.cat_name === category);
    if (!cat) {
        alert("Category not found!");
        return;
    }

    if (!name || !category) { alert('Please fill all fields correctly.'); return; }
    const res = await fetch(API_BASE + 'accounts/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ acc_name: name, cat: cat.id, acc_notes: notes })
    });
    if (res.ok) {
        loadAccounts();
        document.getElementById('account-form').reset();
    }
});


async function loadAccounts() {
    const res = await fetch(API_BASE + 'accounts/');
    const data = await res.json();
    const list = document.getElementById('account-list');
    const accSelect = document.getElementById('transaction-account');
    if (accSelect) accSelect.innerHTML = '';

    list.innerHTML = '';
    data.forEach(acc => {
        const li = document.createElement('li');
        li.textContent = acc.acc_name + ' (Category ID: ' + acc.cat + ') - Notes: ' + acc.acc_notes;
        list.appendChild(li);

        if (accSelect) {
            const opt = document.createElement('option');
            opt.value = acc.acc_name;
            opt.textContent = acc.acc_name;
            accSelect.appendChild(opt);
        }
    });
}

loadCategories();
loadAccounts();

document.getElementById('transaction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const accName = document.getElementById('transaction-account').value;
    const amount = parseFloat(document.getElementById('transaction-amount').value);
    const type = document.getElementById('transaction-type').value;
    const notes = document.getElementById('transaction-notes').value;

    if (!accName || isNaN(amount) || !type) {
        alert("Please fill all fields correctly.");
        return;
    }

    try {
        // Get account ID by name
        const accRes = await fetch(API_BASE + 'accounts/');
        const accData = await accRes.json();
        const acc = accData.find(a => a.acc_name === accName);
        if (!acc) {
            alert("Account not found.");
            return;
        }

        // Get category type ID
        const typeRes = await fetch(API_BASE + 'category-types/');
        const typeData = await typeRes.json();
        const catType = typeData.find(t => t.cat_type === type);
        if (!catType) {
            alert("Transaction type not found.");
            return;
        }

        const response = await fetch(API_BASE + 'transactions/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                acc: acc.id,
                trans_amount: amount,
                cat_type: catType.id,
                trans_notes: notes
            })
        });

        if (response.ok) {
            alert("Transaction added successfully.");
            document.getElementById('transaction-form').reset();
            loadTransactions();
        } else {
            const error = await response.json();
            alert("Error: " + JSON.stringify(error));
        }
    } catch (err) {
        console.error(err);
        alert("An unexpected error occurred.");
    }
});

    if (res.ok) {
        alert("Transaction added successfully.");
        document.getElementById('transaction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const accName = document.getElementById('transaction-account').value;
    const amount = parseFloat(document.getElementById('transaction-amount').value);
    const type = document.getElementById('transaction-type').value;
    const notes = document.getElementById('transaction-notes').value;

    if (!accName || isNaN(amount) || !type) {
        alert("Please fill all fields correctly.");
        return;
    }

    try {
        // Get account ID by name
        const accRes = await fetch(API_BASE + 'accounts/');
        const accData = await accRes.json();
        const acc = accData.find(a => a.acc_name === accName);
        if (!acc) {
            alert("Account not found.");
            return;
        }

        // Get category type ID
        const typeRes = await fetch(API_BASE + 'category-types/');
        const typeData = await typeRes.json();
        const catType = typeData.find(t => t.cat_type === type);
        if (!catType) {
            alert("Transaction type not found.");
            return;
        }

        const response = await fetch(API_BASE + 'transactions/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                acc: acc.id,
                trans_amount: amount,
                cat_type: catType.id,
                trans_notes: notes
            })
        });

        if (response.ok) {
            alert("Transaction added successfully.");
            document.getElementById('transaction-form').reset();
            loadTransactions();
        } else {
            const error = await response.json();
            alert("Error: " + JSON.stringify(error));
        }
    } catch (err) {
        console.error(err);
        alert("An unexpected error occurred.");
    }
});

    if (res.ok) {
        alert("Transaction added successfully.");
        document.getElementById('transaction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const accName = document.getElementById('transaction-account').value;
    const amount = parseFloat(document.getElementById('transaction-amount').value);
    const type = document.getElementById('transaction-type').value;
    const notes = document.getElementById('transaction-notes').value;

    if (!accName || isNaN(amount) || !type) {
        alert("Please fill all fields correctly.");
        return;
    }

    try {
        // Get account ID by name
        const accRes = await fetch(API_BASE + 'accounts/');
        const accData = await accRes.json();
        const acc = accData.find(a => a.acc_name === accName);
        if (!acc) {
            alert("Account not found.");
            return;
        }

        // Get category type ID
        const typeRes = await fetch(API_BASE + 'category-types/');
        const typeData = await typeRes.json();
        const catType = typeData.find(t => t.cat_type === type);
        if (!catType) {
            alert("Transaction type not found.");
            return;
        }

        const response = await fetch(API_BASE + 'transactions/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                acc: acc.id,
                trans_amount: amount,
                cat_type: catType.id,
                trans_notes: notes
            })
        });

        if (response.ok) {
            alert("Transaction added successfully.");
            document.getElementById('transaction-form').reset();
            loadTransactions();
        } else {
            const error = await response.json();
            alert("Error: " + JSON.stringify(error));
        }
    } catch (err) {
        console.error(err);
        alert("An unexpected error occurred.");
    }
});

    if (res.ok) {
        alert("Transaction added successfully.");
        document.getElementById('transaction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const accName = document.getElementById('transaction-account').value;
    const amount = parseFloat(document.getElementById('transaction-amount').value);
    const type = document.getElementById('transaction-type').value;
    const notes = document.getElementById('transaction-notes').value;

    if (!accName || isNaN(amount) || !type) {
        alert("Please fill all fields correctly.");
        return;
    }

    try {
        // Get account ID by name
        const accRes = await fetch(API_BASE + 'accounts/');
        const accData = await accRes.json();
        const acc = accData.find(a => a.acc_name === accName);
        if (!acc) {
            alert("Account not found.");
            return;
        }

        // Get category type ID
        const typeRes = await fetch(API_BASE + 'category-types/');
        const typeData = await typeRes.json();
        const catType = typeData.find(t => t.cat_type === type);
        if (!catType) {
            alert("Transaction type not found.");
            return;
        }

        const response = await fetch(API_BASE + 'transactions/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                acc: acc.id,
                trans_amount: amount,
                cat_type: catType.id,
                trans_notes: notes
            })
        });

        if (response.ok) {
            alert("Transaction added successfully.");
            document.getElementById('transaction-form').reset();
            loadTransactions();
        } else {
            const error = await response.json();
            alert("Error: " + JSON.stringify(error));
        }
    } catch (err) {
        console.error(err);
        alert("An unexpected error occurred.");
    }
});


async function loadTransactions() {
    const res = await fetch(API_BASE + 'transactions/');
    const data = await res.json();
    const list = document.getElementById('transaction-list');
    list.innerHTML = '';
    data.forEach(tx => {
        const li = document.createElement('li');
        li.textContent = `[${tx.trans_date}] ${tx.acc} ${tx.trans_amount} (${tx.cat_type}) - ${tx.trans_notes}`;
        const btn = document.createElement('button');
        btn.textContent = "Delete";
        btn.onclick = async () => {
            if (confirm("Delete this transaction?")) {
                await fetch(API_BASE + 'transactions/' + tx.id + '/', { method: 'DELETE' });
                loadTransactions();
            }
        };
        li.appendChild(btn);
        list.appendChild(li);
    });
}

async function deleteItem(url, id, loader) {
    if (confirm("Are you sure?")) {
        await fetch(API_BASE + url + '/' + id + '/', { method: 'DELETE' });
        loader();
    }
}

function appendDelete(listElem, id, url, loader) {
    const btn = document.createElement('button');
    btn.textContent = "Delete";
    btn.onclick = () => deleteItem(url, id, loader);
    listElem.appendChild(btn);
}

async function loadCategories() {
    const res = await fetch(API_BASE + 'categories/');
    const data = await res.json();
    const list = document.getElementById('category-list');
    const catSelect = document.getElementById('account-category');
    list.innerHTML = '';
    catSelect.innerHTML = '';

    data.forEach(cat => {
        const li = document.createElement('li');
        li.textContent = cat.cat_name + " ";
        appendDelete(li, cat.cat_name, 'categories', loadCategories);
        list.appendChild(li);

        const opt = document.createElement('option');
        opt.value = cat.cat_name;
        opt.textContent = cat.cat_name;
        catSelect.appendChild(opt);
    });
}

async function loadAccounts() {
    const res = await fetch(API_BASE + 'accounts/');
    const data = await res.json();
    const list = document.getElementById('account-list');
    const accSelect = document.getElementById('transaction-account');
    list.innerHTML = '';
    accSelect.innerHTML = '';

    data.forEach(acc => {
        const li = document.createElement('li');
        li.textContent = acc.acc_name + ' (Category ID: ' + acc.cat + ') - Notes: ' + acc.acc_notes + " ";
        appendDelete(li, acc.acc_name, 'accounts', loadAccounts);
        list.appendChild(li);

        const opt = document.createElement('option');
        opt.value = acc.acc_name;
        opt.textContent = acc.acc_name;
        accSelect.appendChild(opt);
    });
}

loadTransactions();
