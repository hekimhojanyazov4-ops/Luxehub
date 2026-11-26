// src/hooks/useRooms.js
import { useEffect, useState } from "react";
import { fetchRooms } from "../lib/rooms";

export function useRooms(filters = {}) {
  const [rooms, setRooms] = useState([]);
  const [count, setCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    fetchRooms(filters)
      .then((data) => {
        if (cancelled) return;
        setRooms(Array.isArray(data) ? data : data.results ?? []);
        setCount(Array.isArray(data) ? data.length : data.count ?? 0);
      })
      .catch((err) => {
        if (cancelled) return;
        setError(err.response?.data?.detail || err.message || "Rooms load error");
      })
      .finally(() => !cancelled && setLoading(false));
    return () => { cancelled = true; };
  }, [JSON.stringify(filters)]);

  return { rooms, count, loading, error };
}