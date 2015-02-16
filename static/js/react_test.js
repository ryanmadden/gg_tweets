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

    if(this.props['award']){
      datalist = <span>{this.props.winner}</span>
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
          <h2 className="award-name">{this.props.award}</h2>
          <h3 className="winner"><i className="fa fa-trophy"></i>{datalist}</h3>
          <h4 className="presenters"><i className="fa fa-microphone"></i>Presented by {presenters}</h4>
          <ul className="nominees">
            <h3 className="awardcategory"><i className="fa fa-certificate"></i>The Other Nominees</h3>
            {nominees}
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
  <DataBox url="thedata.json" pollInterval={1000} />,
  document.getElementById('content')
);


var AImage = React.createClass({
  render: function() {
    return (
      <a href={this.props.href}>
        <img src={this.props.src}/>
      </a>
    );
  }
});

var ImageList = React.createClass({
  render: function() {
    var image_nodes = this.props.data.map(function(obj){
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
        <h2>Click the images to view the best dressed people of the golden globes</h2>
        <h3>images are displayed in order of popularity</h3>
        <ImageList data={this.state.data} />
      </div>
    );
  }
});

React.render(
  <ImageContainer url="best-dressed.json" pollInterval={1000} />,
  document.getElementById('best-dressed-images')
);