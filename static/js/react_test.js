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
      datalist = <li>{this.props.winner}</li>
      nominees = this.props.nominees.map(function(nominee){
        return(
          <li> {nominee} </li>
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
          <ul>
            <h3 className="awardcategory">Nominees</h3>
            {nominees}
          </ul>
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