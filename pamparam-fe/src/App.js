import logo from './logo.svg';
import cat from './cat.png';
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
        <TickerList/>
      </div>
    );
  }
}

class TickerList extends React.Component{
  constructor(props){
    super(props);
    this.state = {value:'nothing', selection:'nothing' ,list: {'nothing':"...","1min":"1 Minute","15min":"15 Minutes","1hr":"1 Hours","4hr":"4 Hours","1d":"1 Day"}};
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);     
  }

  handleChange(event) {    
    this.setState({value: event.target.value});
    //this.setState({selection: 'nothing'});
    }

  handleSubmit(event){
    this.setState({selection: 'nothing'})
    this.setState({selection: this.state.value});
    event.preventDefault();
  }
  render(){
    if(this.state.selection !== 'nothing'){
      return(
        <div>
        <form onSubmit={this.handleSubmit}>
          <label style={{color: "white"}}>
          Select an interval:
          <select className="form-select form-select-lg" onChange={this.handleChange}>
            {Object.keys(this.state.list).map((d,key) => {
              return <option key={key} value = {d}> {this.state.list[d]} </option>;
            })}
          </select>    
          </label>
          <br></br>
          <br></br>
          <input className="btn btn-primary" type="submit" value="Submit" />
        </form>
        <br></br>
        <p style={{color: "white"}}>Currently Displaying: {this.state.selection}</p>
        <ApiCall selection={this.state.selection} />
        </div>
      );
  }
    
    return(<div>
        <form onSubmit={this.handleSubmit}>
          <label style={{ color: "white"}}>
          Select an interval:
          <select className="form-select form-select-lg" onChange={this.handleChange}>
            {Object.keys(this.state.list).map((d,key) => {
              return <option key={key}value = {d}> {this.state.list[d]} </option>;
            })}
          </select> 
          </label>
          <br></br>
          <br></br>
          <input className="btn btn-primary" type="submit" value="Submit" />
        </form>
        <br></br>
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
function ApiCall(props) {
    const [apiData, setApiData] = useState({"loading":{"loading1":"loading","loading2":"loading","loading3":"loading","loading4":"loading","loading5":"loading","loading6":"loading","loading7":"loading"}});
    useEffect(() => {
      setApiData({"loading":{"loading1":"loading","loading2":"loading","loading3":"loading","loading4":"loading","loading5":"loading","loading6":"loading","loading7":"loading"}});
      fetch(props.selection).then(res => res.json()).then(data => {setApiData(data);
      });
    },[props.selection]);


    return(
      <div>
      <p style={{ fontSize:"16px", color:"white" }}>StochRSI=k:d-price:trend,BollingerBands=price:trend,MACD=macd:macd_signal-price:trend,VWAP=vwap-trend:price,UnP&up=Underpriced,OvP&op=overpriced,ne=neutral</p>
      <table style={{ fontSize:"18px" }} className="table table-dark table-hover table-striped table-bordered border-success rounded-3">
        <thead>
          <tr>
          <th scope = "col">Exchange</th>
          <th scope = "col">NVT</th>
          <th scope = "col">StochRSI</th>
          <th scope = "col">BollingerBands</th>
          <th scope = "col">MACD</th>
          <th scope = "col">VWAP</th>
          <th scope = "col">UnP/OvP</th>
          <th scope = "col">Bull/Bear</th>
          </tr>
          {Object.keys(apiData).map((d,key) => {
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
