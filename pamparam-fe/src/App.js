import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from 'react';

class App extends React.Component {

  render(){
    return (
      <div className="App">
        <header className="App-header">
          <Clock />
          <img src={logo} className="App-logo" alt="logo" />
        </header>
        <ApiCall />
      </div>
    );
  }
}
class Clock extends React.Component {
  constructor(props) {
    super(props);
    this.state = {date: new Date()};
  }
  componentDidMount() {
    this.timerID = setInterval(
      () => this.tick(),
      1000
      );
  }

  componentWillUnmount() {
    clearInterval(this.timerID);
  }
  tick() {
    this.setState({date: new Date()});
  }

  render() {
    return(
        <h>{this.state.date.toLocaleTimeString()}</h>
      );
  }
}
function ApiCall() {
    const [apiData, setApiData] = useState({"loading":{"loading":"loading","loading":"loading","signal":"loading"}});
    useEffect(() => {
      fetch('/4hr').then(res => res.json()).then(data => {setApiData(data);
      });
    },[]);



    return(
      <div>
        <p style={{ color: "white"}}>Here is your fucking data.</p>
      <table className="table table-dark">
        <thead>
          <tr>
          <th scope = "col">Coin</th>
          <th scope = "col">%d</th>
          <th scope = "col">%k</th>
          <th scope = "col">Signal</th>
          </tr>
          {Object.keys(apiData).map((d,key) => {
            var asd = apiData[d];
            console.log(asd.signal);


            return(<tr>
            <th key = {key}> {d}</th>
            <ListElement key={key} obj = {apiData[d]}/>
            </tr>);
          })
        }
        </thead>
        <tbody>
        </tbody>
      </table>
      </div>
      );
  }
  function ListElement(props) {
    const obj = props.obj;
    const kk = props.key*100+111;
    return Object.keys(obj).map((d,key) =>
    <th key = {kk}>
      {obj[d]}
    </th>
    );
    
  }

export default App;
