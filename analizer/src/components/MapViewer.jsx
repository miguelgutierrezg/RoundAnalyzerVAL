import { useEffect, useRef, useState } from 'react';
import data from '../data/instants.json';

const mapImages = import.meta.glob('../assets/maps/*.png', { eager: true });

function getMapImage(mapName) {
  const path = `../assets/maps/${mapName}.png`;
  return mapImages[path]?.default;
}

export default function MapViewer({ mapName }) {
  const imgSrc = getMapImage(mapName);
  const imageRef = useRef(null);

  const [tick, setTick] = useState(0);
  const [displaySize, setDisplaySize] = useState({ width: 1, height: 1 });
  const [naturalSize, setNaturalSize] = useState({ width: 1, height: 1 });

  const instants = data.instants;
  const currentTick = instants[tick] || { roundTime: 0, players: [] };
  const players = currentTick.players;

  // Tamaño real de la imagen
  useEffect(() => {
    const img = new Image();
    img.src = imgSrc;
    img.onload = () => {
      setNaturalSize({ width: img.naturalWidth, height: img.naturalHeight });
    };
  }, [imgSrc]);

  // Tamaño visible en pantalla
  useEffect(() => {
    const updateSize = () => {
      if (imageRef.current) {
        const rect = imageRef.current.getBoundingClientRect();
        setDisplaySize({ width: rect.width, height: rect.height });
      }
    };
    updateSize();
    const observer = new ResizeObserver(updateSize);
    if (imageRef.current) observer.observe(imageRef.current);
    return () => observer.disconnect();
  }, []);

  const scaleX = displaySize.width / naturalSize.width;
  const scaleY = displaySize.height / naturalSize.height;

  const handlePrev = () => {
    setTick((prev) => Math.max(prev - 1, 0));
  };

  const handleNext = () => {
    setTick((prev) => Math.min(prev + 1, instants.length - 1));
  };

  return (
    <div className="map-wrapper relative">
      {imgSrc && (
        <img
          ref={imageRef}
          src={imgSrc}
          alt={mapName}
          className="map-image z-0"
        />
      )}

      {/* Jugadores */}
      {players.map((player) => {
        const x = player.location?.x || 0;
        const y = player.location?.y || 0;
        const radians = player.viewRadians ?? 0;
        return (
          <div
            key={player.puuid}
            style={{
              position: 'absolute',
              left: `${x * scaleX}px`,
              top: `${y * scaleY}px`,
              width: '14px',
              height: '14px',
              backgroundColor: 'orange',
              borderRadius: '50%',
              border: '2px solid white',
              transform: `rotate(${radians}rad)`,
              zIndex: 50,
            }}
            title={player.puuid}
          />
        );
      })}

      {/* Evento */}
      {currentTick.event && (
        <div className="absolute top-4 left-1/2 -translate-x-1/2 bg-yellow-200 text-black px-4 py-1 rounded z-50 shadow">
          <strong>Evento:</strong> {currentTick.event.type.toUpperCase()}
        </div>
      )}

      {/* Controles */}
      <div className="absolute bottom-4 left-4 bg-black/70 text-white px-4 py-2 rounded z-50 flex gap-4 items-center">
        <button
          onClick={handlePrev}
          className="bg-gray-700 px-3 py-1 rounded hover:bg-gray-600"
        >
          ⬅
        </button>
        <span>
          Tick {tick + 1} / {instants.length} | Tiempo: {currentTick.roundTime}s
        </span>
        <button
          onClick={handleNext}
          className="bg-gray-700 px-3 py-1 rounded hover:bg-gray-600"
        >
          ➡
        </button>
      </div>
    </div>
  );
}
