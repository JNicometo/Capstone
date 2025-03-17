// This file contains the JavaScript code that handles user input for the year.
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('yearForm');
    const yearInput = document.getElementById('yearInput');
    const result = document.getElementById('result');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const year = yearInput.value;
        result.textContent = `You entered the year: ${year}`;
    });
});

document.getElementById('submitButton').addEventListener('click', async () => {
    const teamAbbr = document.getElementById('teamInput').value;
    const year = document.getElementById('yearInput').value;
    const tableType = document.getElementById('tableTypeInput').value;
    
    // Team data
    const teamsData = {
        "crd": "Arizona_Cardinals", 
        "atl": "Atlanta_Falcons",
        "rav": "Baltimore_Ravens",
        "buf": "Buffalo_Bills",
        "car": "Carolina_Panthers",
        "chi": "Chicago_Bears",
        "cin": "Cincinnati_Bengals",
        "cle": "Cleveland_Browns",
        "dal": "Dallas_Cowboys",
        "den": "Denver_Broncos",
        "det": "Detroit_Lions",
        "gnb": "Green_Bay_Packers",
        "htx": "Houston_Texans",
        "clt": "Indianapolis_Colts",
        "jax": "Jacksonville_Jaguars",
        "kan": "Kansas_City_Chiefs",
        "sdg": "Los_Angeles_Chargers",
        "ram": "Los_Angeles_Rams",
        "mia": "Miami_Dolphins",
        "min": "Minnesota_Vikings",
        "nwe": "New_England_Patriots",
        "nor": "New_Orleans_Saints",
        "nyg": "New_York_Giants",
        "nyj": "New_York_Jets",
        "rai": "Las_Vegas_Raiders",
        "phi": "Philadelphia_Eagles",
        "pit": "Pittsburgh_Steelers",
        "sfo": "San_Francisco_49ers",
        "sea": "Seattle_Seahawks",
        "tam": "Tampa_Bay_Buccaneers",
        "oti": "Tennessee_Titans",
        "was": "Washington_Commanders"
    };

    const teamName = teamsData[teamAbbr];

    // Validate year input
    const currentYear = new Date().getFullYear();
    if (!year || isNaN(year) || year < 1970 || year > currentYear) {
        alert('Please enter a valid year between 1970 and ' + currentYear);
        return;
    }

    if (!teamAbbr || !tableType || !teamName) {
        alert('Please fill in all fields correctly');
        return;
    }

    const url = `http://127.0.0.1:8000/${teamName}/${year}/${tableType}/${teamAbbr}`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        const data = await response.json();
        displayTable(data);
        enableDownloadButton(data);
    } catch (error) {
        document.getElementById('result').innerHTML = `<p>${error.message}</p>`;
        console.error('Error fetching data:', error);
    }
});

function displayTable(data) {
    if (data.length === 0) {
        document.getElementById('result').innerHTML = '<p>No data found</p>';
        return;
    }

    const table = document.createElement('table');
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');

    // Create table headers
    const headers = Object.keys(data[0]);
    const headerRow = document.createElement('tr');
    headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    // Create table rows
    data.forEach(row => {
        const tr = document.createElement('tr');
        headers.forEach(header => {
            const td = document.createElement('td');
            td.textContent = row[header];
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });

    table.appendChild(thead);
    table.appendChild(tbody);
    document.getElementById('result').innerHTML = '';
    document.getElementById('result').appendChild(table);
}

function enableDownloadButton(data) {
    const downloadButton = document.getElementById('downloadButton');
    downloadButton.style.display = 'block';
    downloadButton.onclick = () => downloadCSV(data);
}

function downloadCSV(data) {
    const headers = Object.keys(data[0]);
    const csvRows = [];

    // Add headers
    csvRows.push(headers.join(','));

    // Add rows
    data.forEach(row => {
        const values = headers.map(header => row[header]);
        csvRows.push(values.join(','));
    });

    const csvString = csvRows.join('\n');
    const blob = new Blob([csvString], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', 'data.csv');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}