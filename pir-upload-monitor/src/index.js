const UI = activate require("@syndicate-lang/driver-browser-ui");
// @jsx UI.html
// @jsxFrag UI.htmlFragment

const { WSServer, FromServer, ServerConnected } = activate require("@syndicate-lang/server/lib/client");

assertion type PIR(host, activity);

spawn {
  const addr = WSServer('wss://steam.eighty-twenty.org/syndicate', 'test');
  during ServerConnected(addr) {
    const ui = new UI.Anchor();
    during FromServer(addr, PIR($host, $activity)) {
      assert ui.context(host).html('#main tbody',
                                   <tr>
                                     <td>{host}</td>
                                     <td>{activity}</td>
                                   </tr>);
    }
  }
}
