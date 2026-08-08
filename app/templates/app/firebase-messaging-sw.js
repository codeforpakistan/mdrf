// firebase-messaging-sw.js

importScripts('https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.7.1/firebase-messaging-compat.js');

const firebaseConfig = {
  apiKey: "AIzaSyCxx_31TkpfXlXiBBc53IjtaNzALqsB-Ac",
  authDomain: "code4pk.firebaseapp.com",
  projectId: "code4pk",
  storageBucket: "code4pk.appspot.com",
  messagingSenderId: "344151364555",
  appId: "1:344151364555:web:593724e09714a69f09dc4e",
};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
});

self.addEventListener('notificationclick', function(event) {
    console.log('[Service Worker] Notification click Received.');

    // 1. Close the notification right away
    event.notification.close();

    // 2. Retrieve the link we passed into the 'data' object
    // Fallback to the root '/' if no link was provided
    const targetUrl = event.notification.data?.link || '/';

    // 3. Handle the browser tabs
    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function(clientList) {
            // Check if there is already a tab open for this exact URL
            for (let i = 0; i < clientList.length; i++) {
                const client = clientList[i];
                if (client.url === targetUrl && 'focus' in client) {
                    return client.focus();
                }
            }
            
            // If no tab is currently open to that URL, open a new one
            if (clients.openWindow) {
                return clients.openWindow(targetUrl);
            }
        })
    );
});