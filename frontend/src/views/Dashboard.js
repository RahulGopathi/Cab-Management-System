import { styled } from '@mui/material/styles';
import { useContext, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import useAxios from '../utils/useAxios.js';
import AuthContext from '../contexts/AuthContext';
import {
  MenuItem,
  TextField,
  Stack,
  Select
} from '@mui/material';
import { LoadingButton } from '@mui/lab';
import toast from 'react-hot-toast';
import { GoogleMap, StandaloneSearchBox, DirectionsRenderer, Marker } from '@react-google-maps/api';

const StyledDiv = styled('div')(() => ({
  position: 'absolute',
  marginTop: -22,
  marginLeft: 400,
  top: 90,
}));

const ButtonStyled = styled(LoadingButton)(() => ({
  fontWeight: 700,
  marginRight: 30,
  textTransform: 'none',
  backgroundColor: '#00AB55',
  boxShadow: '0 8px 16px 0 rgba(0, 171, 85, 0.24)',
  '&:hover': {
    backgroundColor: '#007B55',
  },
}));

const StyledTextField = styled(TextField)({
  '& label.Mui-focused': {
    color: '#00AB55',
  },
  '& .MuiInput-underline:after': {
    borderBottomColor: 'green',
  },
  '& .MuiOutlinedInput-root': {
    '& fieldset': {
      borderColor: '#B0B9C2',
    },
    '&:hover fieldset': {
      borderColor: '#000',
    },
    '&.Mui-focused fieldset': {
      borderColor: '#00AB55',
    },
  },
});

const StyledSelectField = styled(Select)({
  '& label.Mui-focused': {
    color: '#00AB55',
  },
  '& .MuiInput-underline:after': {
    borderBottomColor: 'green',
  },
  '& .MuiOutlinedInput-root': {
    '& fieldset': {
      borderColor: '#B0B9C2',
    },
    '&:hover fieldset': {
      borderColor: '#000',
    },
    '&.Mui-focused fieldset': {
      borderColor: '#00AB55',
    },
  },
});

const Dashboard = () => {
  const { setCabDetails } = useContext(AuthContext);
  const navigate = useNavigate();
  const inputStartRef = useRef();
  const inputDropRef = useRef();

  const api = useAxios();
  const [pickupLocation, setPickupLocation] = useState([]);
  const [dropLocation, setDropLocation] = useState([]);
  const [directions, setDirections] = useState(null);
  const [cabType, setCabType] = useState('indi');

  const handleStartPlaceChanged = () => {
    const [place] = inputStartRef.current.getPlaces();
    if (place) {
      console.log(place.formatted_address)
      console.log(place.geometry.location.lat())
      console.log(place.geometry.location.lng())
      setPickupLocation([place.geometry.location.lat(), place.geometry.location.lng()])
    }
  }

  const handleDropPlaceChanged = () => {
    const [place] = inputDropRef.current.getPlaces();
    if (place) {
      console.log(place.formatted_address)
      console.log(place.geometry.location.lat())
      console.log(place.geometry.location.lng())
      setDropLocation([place.geometry.location.lat(), place.geometry.location.lng()])
    }
  }

  const calculateDirections = (origin, destination) => {
    const directionsService = new window.google.maps.DirectionsService();

    directionsService.route(
      {
        origin: origin,
        destination: destination,
        travelMode: window.google.maps.TravelMode.DRIVING,
      },
      (result, status) => {
        if (status === window.google.maps.DirectionsStatus.OK) {
          setDirections(result);
        } else {
          console.error(`Error fetching directions: ${status}`);
        }
      }
    );
  };

  const assignCab = async () => {
    if (cabType === "indi") {
      try {
        const response = await api.post('/assign_cab/', {
          "pickup_latitude": pickupLocation[0],
          "pickup_longitude": pickupLocation[1],
          "drop_latitude": dropLocation[0],
          "drop_longitude": dropLocation[1]
        });
        console.log(response)
        if (!response.data.error) {
          toast.success('Cab Booked Successfully');
          setCabDetails(response.data);
          setTimeout(() => {
            navigate('/myTrip');
          }, 2000);
        }
        else {
          toast.error('No cabs available');
        }
      }
      catch {
        console.log('Something went wrong');
        toast.error('Something went wrong');
      }
    }
    else {
      try {
        const response = await api.post('/assign_sharing_cab/', {
          "pickup_latitude": pickupLocation[0],
          "pickup_longitude": pickupLocation[1],
          "drop_latitude": dropLocation[0],
          "drop_longitude": dropLocation[1],
        });
        console.log(response)
        if (!response.data.error) {
          toast.success('Cab Booked Successfully');
          setCabDetails(response.data);
          setTimeout(() => {
            navigate('/myTrip');
          }, 2000);
        }
        else {
          toast.error('No cabs available');
        }
      }
      catch {
        console.log('Something went wrong');
        toast.error('Something went wrong');
      }
    }
  }

  return (
    <StyledDiv>
      <h1>Book a Cab</h1>
      <div style={{ height: 550, width: 870, textAlign: 'center' }}>
        <Stack spacing={3}>
          <Stack direction="row" spacing={3}>
            <StandaloneSearchBox
              onLoad={ref => inputStartRef.current = ref}
              onPlacesChanged={handleStartPlaceChanged}
            >
              <StyledTextField
                required
                label="Start Location"
                variant="outlined"
                sx={{
                  width: 320,
                  typography: 'body1',
                  input: { color: '#000' },
                }}
              />
            </StandaloneSearchBox>
            <StandaloneSearchBox
              onLoad={ref => inputDropRef.current = ref}
              onPlacesChanged={handleDropPlaceChanged}
            >
              <StyledTextField
                required
                label="Drop Location"
                variant="outlined"
                sx={{
                  width: 320,
                  typography: 'body1',
                  input: { color: '#000' },
                }}
              />
            </StandaloneSearchBox>
            <StyledSelectField
              value={cabType}
              label="Type of Cab"
              onChange={(e) => setCabType(e.target.value)}
            >
              <MenuItem value={"indi"}>Individual</MenuItem>
              <MenuItem value={"sharing"}>Sharing</MenuItem>
            </StyledSelectField>
            <ButtonStyled
              sx={{ marginTop: 2, marginRight: 0, marginBottom: 10 }}
              size="large"
              variant="contained"
              onClick={() => {
                console.log('clicked');
                calculateDirections(
                  inputStartRef.current.getPlaces()[0].geometry.location,
                  inputDropRef.current.getPlaces()[0].geometry.location
                );
                assignCab();
              }}
            >
              Book
            </ButtonStyled>
          </Stack>
          <GoogleMap
            mapContainerStyle={{ width: 870, height: 550 }}
            center={{ lat: 17.4065, lng: 78.4772 }}
            zoom={10}
          >
            {directions && (
              <>
                <DirectionsRenderer
                  directions={directions}
                  options={{
                    polylineOptions: {
                      strokeColor: 'blue',
                    },
                    suppressMarkers: true,
                  }}
                />
                <Marker position={directions.routes[0].legs[0].start_location}
                  label="Start"
                  labelColor="white"
                  icon={{
                    url: 'https://i.imgur.com/K0RDsqf.png',
                    scaledSize: new window.google.maps.Size(60, 60),
                  }} />
                <Marker position={directions.routes[0].legs[0].end_location}
                  label="Drop"
                  labelColor="white"
                  icon={{
                    url: 'https://i.imgur.com/9a0toB4.png',
                    scaledSize: new window.google.maps.Size(60, 60),
                  }} />
                <Marker position={directions.routes[0].legs[0].start_location}
                  icon={{
                    url: 'https://i.imgur.com/Dwim9LL.png',
                    scaledSize: new window.google.maps.Size(60, 60),
                  }} />
              </>
            )}
          </GoogleMap>
        </Stack>
      </div>
    </StyledDiv>
  );
};

export default Dashboard;
