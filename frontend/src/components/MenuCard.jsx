import { useState } from "react";
import { itemDetails } from "../starterMenu";

export default function MenuCard({ item, onAdd }) {
  // TODO-WORKSHOP-1
  const [showDetails, setShowDetails] = useState(false);

  return (
    <article className="card">
      <h2>{item.name}</h2>
      <p className="price">${item.price}</p>
      {/* TODO-WORKSHOP-8
          When item.available === false, show <p className="sold-out">SOLD OUT</p>
          and disable the Add to Order button. */}
      <div className="card-actions">
        <button
          type="button"
          onClick={() => {
            // TODO-WORKSHOP-1
            setShowDetails((current) => !current);
          }}
        >
          {showDetails ? "Hide details" : "View details"}
        </button>
        <button type="button" onClick={() => onAdd(item)}>
          Add to Order
        </button>
      </div>
      {showDetails ? <p className="details">{itemDetails[item.id]}</p> : null}
    </article>
  );
}
