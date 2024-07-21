// // components/StripeButton.js
// 'use client';
// import { loadStripe } from '@stripe/stripe-js';
// import React from 'react';
// import Stripe from 'stripe';

// const stripePromise = loadStripe(
//   'pk_test_51NJdQ5EeY9w1Ijmkh5n4I6pybkz9f5lH3fs1XuiynFYQziamVAdUnDAPqIwonxmwDPcZyahzMJkS1e1F17TvWs7R00olOzNNiN'
// );

// // const StripeButton = () => {
// //   // PublicKey
// //   const stripe = new Stripe(
// //     'pk_test_51NJdQ5EeY9w1Ijmkh5n4I6pybkz9f5lH3fs1XuiynFYQziamVAdUnDAPqIwonxmwDPcZyahzMJkS1e1F17TvWs7R00olOzNNiN'
// //   );
//   const handleButtonClick = async () => {
//     try {
//       const response = await fetch(
//         'http://127.0.0.1:8004/payment/create-checkout-session',
//         {
//           method: 'POST',
//           headers: {
//             'Content-Type': 'application/json',
//           },
//           body: JSON.stringify({ key: 'Sarim' }), // Replace with your data
//         }
//       );

//       if (response.ok) {
//         console.log('Data sent successfully!');
//       } else {
//         console.error('Error sending data:', response.statusText);
//       }
//     } catch (error) {
//       console.error('Network error:', error);
//     }
//   };

//   return <button onClick={handleButtonClick}>Send Data to FastAPI</button>;
// };

// export default StripeButton;
