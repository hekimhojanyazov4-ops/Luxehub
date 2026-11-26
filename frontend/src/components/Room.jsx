// src/components/RoomCard.jsx
import React from "react";

export default function RoomCard({ room }) {
  const price = Number(room.price_per_night ?? 0).toFixed(0);
  const image = room.images?.[0]?.image || room.images?.[0]?.url || null;
  const avgRating = room.average_rating ?? room.avg_rating ?? null;

  return (
    <article style={styles.card}>
      <div style={styles.imageWrap}>
        {image ? (
          <img
            src={image}
            alt={room.name || room.room_type}
            style={styles.image}
          />
        ) : (
          <div style={styles.imagePlaceholder}>
            {room.room_type?.toUpperCase() || "ROOM"}
          </div>
        )}
        {!room.is_active && <span style={styles.badge}>INACTIVE</span>}
      </div>
      <div style={styles.body}>
        <h3 style={styles.title}>
          {room.name || `${room.room_type} #${room.room_number}`}
        </h3>
        <p style={styles.meta}>
          {room.capacity} guests · {room.room_type}
        </p>
        {avgRating != null && (
          <p style={styles.rating}>★ {Number(avgRating).toFixed(1)}</p>
        )}
        <div style={styles.footer}>
          <span style={styles.price}>
            ${price}
            <small>/night</small>
          </span>
        </div>
      </div>
    </article>
  );
}

const styles = {/* neon/simple */};
