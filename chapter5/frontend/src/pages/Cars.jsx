import Layout from "../components/Layout";
import Card from "../components/Card";
import { useState, useEffect } from "react";

const Cars = () => {
  const [cars, setCars] = useState([]);
  const [brand, setBrand] = useState("");
  const [isPending, setIsPending] = useState(true);

  useEffect(() => {
    fetch(`http://localhost:8000/cars?brand=${brand}`)
      .then((respose) => respose.json())
      .then((json) => {
        setCars(json.cars)
    });
    setIsPending(false);
  }, [brand]);

  const handleChangeBrand = (event) => {
    setCars([]);
    setBrand(event.target.value);
    setIsPending(true);
  };

  return (
    <Layout>
      <h2 className="font-bold font-mono text-lg text-center my-4">Cars - {brand ? brand : "all brands"}</h2>
      <div>
        <label htmlFor="cars">Choose a brand: </label>
        <select name="cars" id="cars" onChange={handleChangeBrand}>
          <option value="">All cars</option>
          <option value="Fiat">Fiat</option>
          <option value="Citroen">Citroen</option>
          <option value="Renault">Renault</option>
          <option value="Opel">Opel</option>
          <option value="Toyota">Toyota</option>
        </select>
      </div>
      <div>
        {isPending && (
          <div>
            <h2>Loading cars, brand:{brand}...</h2>
          </div>
        )}
        <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
          { cars &&
            cars.map((el) => {
              return <Card key={el.id} car={el} />;
            })}
        </div>
      </div>
    </Layout>
  );
};
export default Cars;
