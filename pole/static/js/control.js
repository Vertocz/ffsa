// Variables globales pour les chronos
let matchTime = 10 * 60;  // Temps du match en secondes (10 minutes)
let matchMilliseconds = 0;  // Millisecondes pour le match (pour la précision des dixièmes)
let matchTimeRunning = false;  // Si le chrono du match est en cours
let matchInterval = null;  // Intervalle pour mettre à jour le chrono du match

let possessionTime = 12;  // Temps de possession en secondes
let possessionMilliseconds = 0;  // Millisecondes pour la possession (pour la précision des dixièmes)
let possessionTimeRunning = false;  // Si le chrono de possession est en cours
let possessionInterval = null;  // Intervalle pour mettre à jour le chrono de possession





let matchId = "match1"; // L'identifiant du match à contrôler
const controlSocket = new WebSocket(`ws://127.0.0.1:8000/ws/match/${matchId}/`);

// Fonction pour envoyer des mises à jour
function sendUpdate(data) {
    controlSocket.send(JSON.stringify(data));
}

// Exemple : Mise à jour du score
function updateScore(team, points) {
    sendUpdate({ type: "score", team: team, points: points });
}

// Gestion des erreurs et de la connexion
controlSocket.onopen = function() {
    console.log("WebSocket connecté au match " + matchId);
};

controlSocket.onclose = function() {
    console.log("WebSocket déconnecté");
};






// Fonction pour démarrer/arrêter le chrono du match
function startStopMatch() {
    if (matchTimeRunning) {
        clearInterval(matchInterval);
        document.getElementById("start-stop").textContent = "Start";
    } else {
        matchInterval = setInterval(runMatchTime, 100);  // Mise à jour toutes les 100ms (dixièmes de seconde)
        document.getElementById("start-stop").textContent = "Stop";
    }

    matchTimeRunning = !matchTimeRunning;
}

// Fonction pour mettre à jour le chrono du match
function runMatchTime() {
    // Décrémenter les millisecondes du match
    if (matchMilliseconds === 0) {
        if (matchTime > 0) {
            matchTime--;  // Décrémenter le temps du match d'une seconde
        }
        matchMilliseconds = 9;  // Réinitialiser les millisecondes à 9 (fin du dixième de seconde précédent)
    } else {
        matchMilliseconds--;  // Décrémenter les dixièmes de seconde
    }

    // Format du temps de match (en minutes:secondes.dixièmes)
    const minutes = Math.floor(matchTime / 60);
    const seconds = matchTime % 60;
    document.getElementById("match-time").textContent = `${minutes}:${seconds < 10 ? '0' + seconds : seconds}.${matchMilliseconds}`;
}

// Fonction pour ajuster le temps du match (+1 ou -1)
function adjustTime(type, value) {
    if (type === 'match') {
        matchTime += value;
        if (matchTime < 0) matchTime = 0;  // Ne pas autoriser des valeurs négatives
        const minutes = Math.floor(matchTime / 60);
        const seconds = matchTime % 60;
        document.getElementById("match-time").textContent = `${minutes}:${seconds < 10 ? '0' + seconds : seconds}.${matchMilliseconds}`;
    } else if (type === 'possession') {
        possessionTime += value;
        if (possessionTime < 0) possessionTime = 0;  // Ne pas autoriser des valeurs négatives
        document.getElementById("possession-time").textContent = `${possessionTime}.${possessionMilliseconds}`;
    }
}

function startStopPossession() {
    if (possessionTimeRunning) {
        clearInterval(possessionInterval);
        document.getElementById("possession-start-stop").textContent = "Start";
    } else {
        // Si le chrono est à 0, réinitialiser à 12.0 avant de démarrer
        if (possessionTime <= 0 && possessionMilliseconds <= 0) {
            possessionTime = 12;
            possessionMilliseconds = 0;
        }
        possessionInterval = setInterval(runPossessionTime, 100);  // Mise à jour toutes les 100ms
        document.getElementById("possession-start-stop").textContent = "Stop";
    }

    possessionTimeRunning = !possessionTimeRunning;
}


// Fonction pour mettre à jour le chrono de possession
function runPossessionTime() {
    // Décrémenter les millisecondes de possession
    if (possessionMilliseconds === 0) {
        if (possessionTime > 0) {
            possessionTime--;  // Décrémenter le temps de possession d'une seconde
        }
        possessionMilliseconds = 9;  // Réinitialiser les millisecondes à 9 (fin du dixième de seconde précédent)
    } else {
        possessionMilliseconds--;  // Décrémenter les dixièmes de seconde
    }

    // Si le temps de possession atteint 0, arrêter le chrono
    if (possessionTime <= 0 && possessionMilliseconds <= 0) {
        clearInterval(possessionInterval);
        possessionTimeRunning = false;
        document.getElementById("possession-start-stop").textContent = "Start";  // Remettre le bouton à "Start"
    }

    // Format du temps de possession (en secondes.dixièmes)
    document.getElementById("possession-time").textContent = `${possessionTime}.${possessionMilliseconds}`;
}


// Fonction pour réinitialiser le chrono de possession
function resetPossession() {
    if (possessionTimeRunning) {
        possessionTime = 12;  // Si le chrono tourne, réinitialiser à 12 et démarrer
        possessionMilliseconds = 0;
        document.getElementById("possession-time").textContent = `${possessionTime}.${possessionMilliseconds}`;
    } else {
        possessionTime = 12;  // Réinitialiser sans démarrer
        possessionMilliseconds = 0;
        document.getElementById("possession-time").textContent = `${possessionTime}.${possessionMilliseconds}`;
    }
}

// Fonction pour mettre à jour le score d'une équipe
function updateTeam(team, points) {
    const teamScoreElement = document.getElementById(team + '-score');
    let currentScore = parseInt(teamScoreElement.textContent.replace('Score: ', ''));
    currentScore += points;
    if (currentScore < 0) currentScore = 0;  // Le score ne peut pas être négatif
    teamScoreElement.textContent = 'Score: ' + currentScore;
}

// Fonction pour mettre à jour les fautes d'une équipe
function updateFouls(team, fouls) {
    const teamFoulsElement = document.getElementById(team + '-fouls');
    let currentFouls = parseInt(teamFoulsElement.textContent.replace('Fautes: ', ''));
    currentFouls += fouls;
    if (currentFouls < 0) currentFouls = 0;  // Les fautes ne peuvent pas être négatives
    teamFoulsElement.textContent = 'Fautes: ' + currentFouls;

    // Appliquer la couleur des fautes
    if (currentFouls < 6) {
        teamFoulsElement.style.color = "green";
    } else if (currentFouls < 7) {
        teamFoulsElement.style.color = "orange";
    } else if (currentFouls < 10) {
        teamFoulsElement.style.color = "red";
    } else {
        teamFoulsElement.style.color = "violet";
    }
}

function openDisplay() {
    // Ouvre la page d'affichage dans une nouvelle fenêtre
    window.open('/display/', '_blank', 'width=800,height=600');
}
