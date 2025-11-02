// This file is intentionally left blank.

document.addEventListener('DOMContentLoaded', () => {
  const liveBtn = document.getElementById('liveCapture');
  if (!liveBtn) return;

  liveBtn.addEventListener('click', async () => {
    liveBtn.disabled = true;
    try {
      const res = await fetch('/start_stream', { method: 'POST' });
      if (!res.ok) {
        const body = await res.json().catch(() => ({ error: 'start failed' }));
        alert('Could not start camera: ' + (body.error || res.status));
        liveBtn.disabled = false;
        return;
      }
      // camera started, go to live page which will attach the MJPEG feed
      window.location.href = '/live';
    } catch (e) {
      alert('Error starting camera: ' + e.message);
      liveBtn.disabled = false;
    }
  });
});