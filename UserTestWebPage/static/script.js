document.addEventListener('DOMContentLoaded', function () {

    let timerInterval = null;
    let timingStarted = false; // To track the state of timing
    const maxTime = 600; // 10 minutes in seconds

    const timingBtn = document.getElementById('timingBtn');
    const skipBtn = document.getElementById('skipBtn');
    const taskIdInput = document.getElementById('taskId');

    function updateTimeDisplay(minutes, seconds) {
        document.getElementById('timer').textContent = `${minutes}m:${seconds}s`;
    }

    function toggleTiming() {
        if (!timingStarted) {
            startTiming();
            timingBtn.textContent = 'Finish';
            timingStarted = true;
        } else {
            endTiming(true); // true indicates the task was completed
            timingBtn.textContent = 'Start Timing';
            timingStarted = false;
        }
    }

    function startTiming() {
        let secondsPassed = 0;
        timerInterval = setInterval(() => {
            secondsPassed++;
            const minutes = Math.floor(secondsPassed / 60);
            const seconds = secondsPassed % 60;
            updateTimeDisplay(minutes, seconds);

            if (secondsPassed >= maxTime) {
                endTiming(true); // Automatically end the task if max time is reached
            }
        }, 1000);

        startTask();
    }

    function endTiming(taskCompleted) {
        clearInterval(timerInterval);
        endTask(taskCompleted);
    }

    function skipTask() {
        clearInterval(timerInterval);
        endTask(false); // false indicates the task was skipped
        timingStarted = false;
        timingBtn.textContent = 'Start Timing';
    }

    // Start/Skip button event listeners
    timingBtn.addEventListener('click', toggleTiming);
    skipBtn.addEventListener('click', skipTask);

    function startTask() {
        startTime = new Date().toISOString();
        console.log('Task started:', startTime); // Placeholder for actual functionality
    }

    function endTask(taskCompleted) {
        const endTime = new Date().toISOString();
        const duration = (new Date(endTime) - new Date(startTime)) / 1000; // Duration in seconds
        console.log('Task ended:', endTime, 'Duration:', duration); // Placeholder for actual functionality

        fetch('/record_timing', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                taskId: taskIdInput.value,
                deviceId: currentDeviceId,
                startTime: startTime,
                endTime: endTime,
                duration: duration,
                taskCompleted: taskCompleted
            }),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Timing data recorded:', data);
                if (taskCompleted) {
                    document.getElementById('congratsMessage').style.display = 'block';
                }
                // Logic to navigate to next task or update UI accordingly
            })
            .catch(error => console.error('Error:', error));

        //hide button with id 'timingBtn' and 'skipBtn', and show button with id 'continueBtn'
        document.getElementById('timingBtn').style.display = 'none';
        document.getElementById('skipBtn').style.display = 'none';
        document.getElementById('continueBtn').style.display = 'block';
    }

    function goToNextStep() {
        fetch('/next_step', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                userId: userId, // Make sure you have user ID available
                currentDeviceId: currentDeviceId, // Current device ID
                currentTaskId: taskIdInput.value // Current task ID
            }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.action === 'next_task') {
                    window.location.href = `/device/${data.deviceId}/task/${data.taskId}`;
                } else if (data.action === 'next_device') {
                    window.location.href = `/device/${data.deviceId}`;
                } else if (data.action === 'complete') {
                    window.location.href = '/study_complete';
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Bind this function to the "Continue" button's click event
    continueBtn.addEventListener('click', function () {
        goToNextStep();
    });

});
