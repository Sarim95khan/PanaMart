'use client';
import { getStripePromise } from './getStripPromise';

const Checkout = () => {
  // console.log(getStripePromise);
  const handleCheckout = async () => {
    const stripe = await getStripePromise();
    console.log('Stripe');
    const res = await fetch(
      'http://127.0.0.1:8004/payment/create-checkout-session',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ key: 'Value' }),
        cache: 'no-cache',
      }
    );

    console.log('Response', res);
    const stripeData = await res.json();
    console.log('Stripe Data', stripeData);
    if (stripeData.session) {
      //   stripe?.redirectToCheckout({ sessionId: stripeData.url });

      //   stripe?.redirectToCheckout({ sessionId: stripeData.session.id });
      window.location.href = stripeData.session.url;
    }
  };

  return (
    <div className="py-5">
      <button className="bg-green-200 p-3 rounded-md" onClick={handleCheckout}>
        Checkout
      </button>
    </div>
  );
};

export default Checkout;
