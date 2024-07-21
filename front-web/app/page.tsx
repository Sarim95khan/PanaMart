import Image from 'next/image';
import Checkout from './Checkout.';

export default function Home() {
  return (
    <main className="flex flex-col justify-center items-center h-full mt-10">
      <h1 className="text-3xl font-bold">I am Sarim Mart Service</h1>
      <Checkout />
    </main>
  );
}
