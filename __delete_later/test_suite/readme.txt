• Spin up N simulated students (browser contexts).
• Each student:
	◦ Navigates to the tutor app.
	◦ Submits a metaphor response.
	◦ Waits for tutor feedback (concept/scaffold).
	◦ Optionally stalls to trigger the hint system.
• Collect metrics: response time, success/failure, concurrency limits.

npx playwright test