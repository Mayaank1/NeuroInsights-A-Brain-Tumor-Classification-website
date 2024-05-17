
import images from './images.jpg'

const MapOne = () => {
  return (
    <div className="col-span-12 rounded-sm h-100 border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark xl:col-span-7">
      {/* <h4 className="mb-2 text-xl font-semibold text-black dark:text-white"> */
      <img  className="w-full h-full object-cover rounded-sm"src={images} alt="" />
      }
      
      
    </div>
  );
};

export default MapOne;
