var Data = React.createClass({
  render: function() {
    datalist = null 
    nominees = null
    presenters = null 
    if(this.props['hosts']){
      datalist = this.props.hosts.map(function(host){
        return (
          <li> {host} </li>
        );
      });
      return (
        <div className="data">
          <h2 className="dataaward"></h2>
          {datalist}
        </div>
      );
    }

    console.log('hello')
    if(this.props['award']){
      datalist = <li>{this.props.winner}</li>
      console.log(this.props.nominees)
      nominees = this.props.nominees.map(function(nominee){
        return(
          <li>{nominee}</li>
          );
      });
      presenters = this.props.presenters.map(function(presenter){
        return(
          <li> {presenter} </li>
          );
      });

      return (
        <div className="data">
          <h2 className="dataaward">
            {this.props.award}
          </h2>
          <ul>
            <h3 className="awardcategory">Winner</h3>
            {datalist}
          </ul>
          <ol>
            <h3 className="awardcategory">Nominees</h3>
            {nominees}
          </ol>
          <ul>
            <h3 className="awardcategory">Presenters</h3>
            {presenters}
          </ul>
        </div>
      );
    }

    return (
      <div className="data">
        <h2 className="dataaward"></h2>
      </div>
    );
  }
});

var DataList = React.createClass({
  render: function() {
  	var data_nodes = this.props.data.map(function(data){
      if(data['award']){
        return (
          <Data award={data.award} winner={data.winner} nominees={data.nominees} presenters={data.presenters}>
            {data.winner}
         </Data>
       );
      }
      else if (data['hosts']){
        return (
        <div>
          <h1>Hosts</h1>
          <Data hosts={data.hosts}>
            {data.hosts}
          </Data>
        </div>
        );
      }

  		return (
  			<Data hosts={data.hosts} award={data.award} winner={data.winner}>
          {data.hosts}
          {data.award}
  				{data.winner}
          }
        }
  			</Data>
  		);
  	});
    return (
      <div className="DataList">
        {data_nodes}
      </div>
    );
  }
});

var DataBox = React.createClass({
  load_data: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {data: []};
  },
  componentDidMount: function() {
    this.load_data();
    setInterval(this.load_data, this.props.pollInterval);
  },
  render: function() {
    return (
      <div className="DataBox">
        <DataList data={this.state.data} />
      </div>
    );
  }
});

React.render(
  <DataBox url="thedata.json" pollInterval={2000} />,
  document.getElementById('content')
);


var AImage = React.createClass({
  render: function() {
    return (
      <a href={this.props.link}>
        <img src={this.props.src}/>
      </a>
    );
  }
});

var ImageList = React.createClass({
  render: function() {
    console.log(this.props);
    console.log(this.props.data);
    var image_nodes = this.props.data.map(function(obj){
      console.log(obj);
      return (
        <li>
          <AImage src={obj.img} href={obj.link}>
            {obj.img}
          </AImage>
        </li>
      );
    });

    return (
      <div className="images-list">
        <ul className="ImageList small-block-grid-3">
          {image_nodes}
        </ul>
      </div>
    );
  }
});

var ImageContainer = React.createClass({
  load_data: function() {
    console.log('loading data');
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {data: []};
  },
  componentDidMount: function() {
    this.load_data();
    setInterval(this.load_data, this.props.pollInterval);
  },
  render: function() {
    return (
      <div className="ImageContainer">
        <ImageList data={this.state.data} />
      </div>
    );
  }
});

React.render(
  <ImageContainer url="best-dressed.json" pollInterval={2000} />,
  document.getElementById('best-dressed-images')
);