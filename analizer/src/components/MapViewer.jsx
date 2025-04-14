const mapImages = import.meta.glob('../assets/maps/*.png', { eager: true });

function getMapImage(mapName) {
  const path = `../assets/maps/${mapName}.png`;
  return mapImages[path]?.default;
}

export default function MapViewer({ mapName }) {
  const imgSrc = getMapImage(mapName);

  return (
    <div className="map-wrapper">
      {imgSrc && <img src={imgSrc} alt={mapName} className="map-image" />}
    </div>
  );
}
